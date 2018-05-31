# Usage
Install dependencies e.g.:
```
sudo pacman -S mono nuget
```
Install HtmlAgilityPack.
This will download the packages to the current directory:
```
nuget install HtmlAgilityPack
```
Make sure that the paths to HtmlAgilityPack.dll is correct.
Compile:
```
msc crawler.cs -r:System.Net.Http -reference:HtmlAgilityPack.1.8.4/lib/Net40/HtmlAgilityPack.dll
```
Run:
```
MONO_PATH=./HtmlAgilityPack.1.8.4/lib/Net40/ mono crawler.exe
```
