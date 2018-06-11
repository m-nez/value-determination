using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using HtmlAgilityPack;

namespace MSSQL
{
    class Raport
    {
        public int NbElement { get; }
        public string Name { get; }

        public double Price { get; set; }
        public long NumberShares { get; set; }

        public string Shares { get; set; }



        private long []Values;
        public Raport(string name)
        {
            Name = name;
            NbElement = 17;

            Values = new long[NbElement];
            Price = 0;
        }

        public void Set(int i, long v)
        {
            Values[i] = v;
        }

        public long Get(int i)
        {
            return Values[i];
        }
    }
    class Program
    {
        private static List<string> GetCompaniesLinks(string url)
        {
            List<string> CompaniesLinks = new List<string>();

            HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create(url);
            WebResponse response = request.GetResponse();
            Stream stream = response.GetResponseStream();

            HtmlDocument doc = new HtmlDocument();

            doc.Load(stream);
            HtmlNodeCollection links = doc.DocumentNode.SelectNodes("//td/a[@class]");
            foreach (HtmlNode element in links)
            {
                CompaniesLinks.Add(element.Attributes["href"].Value.Split('/')[2]);
            }

            return CompaniesLinks;
        }

        private static List<Raport> GetCompanyRaports(string name)
        {
            List<Raport> CompanyRaports = new List<Raport>();

            HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create("https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/" + name + ",Q");
            WebResponse response = request.GetResponse();
            Stream stream = response.GetResponseStream();

            HtmlDocument doc = new HtmlDocument();

            doc.Load(stream);

            HtmlNodeCollection r = doc.DocumentNode.SelectNodes("//table[@class='report-table']");
            HtmlNode raport = r[0];

            //nazwy kwartałów
            HtmlNodeCollection rh = raport.SelectNodes("//th[@class='thq h'] | //th[@class='thq h newest']");
            foreach (HtmlNode element in rh)
            {
                string namen = element.InnerHtml;
                namen = Regex.Replace(namen, @"\s", "");

                CompanyRaports.Add(new Raport(namen));
            }

            HtmlNodeCollection tr = raport.SelectNodes(".//tr ");
            tr.Remove(0);

            int i = 0;
            foreach (HtmlNode element in tr)
            {
                HtmlNodeCollection rSpan = element.SelectNodes(".//span[@class='value']/span/span");

                int j = 0;

                if (i == CompanyRaports[j].NbElement)
                {
                    return null;
                }

                foreach (HtmlNode value in rSpan)
                {
                    string v = value.InnerHtml;
                    v = Regex.Replace(v, @"\s", "");

                    CompanyRaports[j].Set(i, Convert.ToInt64(v));
                    j++;
                }

                //System.Console.Write(i);


                i++;
            }

            request = (HttpWebRequest)HttpWebRequest.Create("https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/" + name + ",0");
            response = request.GetResponse();
            stream = response.GetResponseStream();

            doc = new HtmlDocument();

            doc.Load(stream);

            //kurs akcji
            r = doc.DocumentNode.SelectNodes("//table[@class='report-table']//tr");

            List<double> prices =  new List<double>();

            foreach (var p in r[1].SelectNodes(".//td"))
            {
                string price = p.InnerText.Trim();
                if(price != "")
                {
                    try
                    {
                        double pp = Convert.ToDouble(price);
                        prices.Add(pp);
                    }
                    catch (FormatException){ }
                }
            }

            for (int j = 0; j < prices.Count; j++)
                CompanyRaports[CompanyRaports.Count - j - 1].Price = prices[prices.Count - j - 1];

            //ilość akcji
            r = doc.DocumentNode.SelectNodes("//table[@class='report-table']//tr");

            List<long> numbers = new List<long>();

            foreach (var n in r[2].SelectNodes(".//td"))
            {
                string number = n.InnerText.Trim();
                if (number != "")
                {
                    try
                    {
                        number = number.Replace(" ", "");
                        long nn = Convert.ToInt64(number);
                        numbers.Add(nn);
                    }
                    catch (FormatException) { }
                }
            }

            for (int j = 0; j < numbers.Count; j++)
                CompanyRaports[CompanyRaports.Count - j - 1].NumberShares = numbers[numbers.Count - j - 1];

            return CompanyRaports.GetRange(5, CompanyRaports.Count-5);
        }

        static void Main(string[] args)
        {
             List<string> CompaniesLinks = GetCompaniesLinks("https://www.biznesradar.pl/gielda/indeks:WIG20");

              if (!Directory.Exists("raporty"))
              {
                  Directory.CreateDirectory("raporty");
              }

              int i = 1;
              int len = CompaniesLinks.Count();

              foreach (string name in CompaniesLinks)
              {
                  System.Console.WriteLine(name + " (" + i + " / " + len + ")" );

                  StreamWriter sw = File.CreateText("raporty/" + name + ".csv");
                  string header = "Kwartał,Przychody ze sprzedaży,Techniczny koszt wytworzenia produkcji sprzedanej,Koszty sprzedaży,Koszty ogólnego zarządu,Zysk ze sprzedaży,Pozostałe przychody operacyjne,Pozostałe koszty operacyjne,Zysk operacyjny (EBIT),Przychody finansowe,Koszty finansowe,Pozostałe przychody (koszty),Zysk z działalności gospodarczej,Wynik zdarzeń nadzwyczajnych,Zysk przed opodatkowaniem,Zysk (strata) netto z działalności zaniechanej,Zysk netto,Zysk netto akcjonariuszy jednostki dominującej,Kurs,Ilość akcji";

                  List<Raport> CompanyRaports = GetCompanyRaports(name);
                  
                  if(CompanyRaports == null)
                  {
                      sw.Close();
                      File.Delete("raporty/" + name + ".csv");
                      i++;
                      continue;
                  }
                  sw.WriteLine(header);

                  foreach (Raport element in CompanyRaports)
                  {
                       sw.Write(element.Name);

                       for (int j = 0; j < element.NbElement; j++)
                            sw.Write("," + element.Get(j));

                       sw.Write("," + element.Price);
                       sw.Write("," + element.NumberShares);
                       sw.WriteLine();
                  }

                  sw.Close();
                  i++;
              }

             System.Console.WriteLine("Downloaded!");
             Console.ReadLine();
        }
    }
}
