using HtmlAgilityPack;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using RestSharp.Contrib;
using Syncfusion.Windows.Forms;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using System.Threading;

namespace ShopwareGrabber
{
    public class ShopMediamarkt : Shop
    {
  //      IWebDriver MediaDriver;
        public ShopMediamarkt(string name, string domain) : base(name, domain)
        {

        }

        public override bool HideExtra()
        {
            return false;
        }

        public override Produkt Parse(string html)
        {
            var htmlDoc = new HtmlAgilityPack.HtmlDocument();

            try
            {
                htmlDoc.LoadHtml(html);

                string price = "", priceRegular = "";

                if (htmlDoc.QuerySelectorAll("span[font-family=\"price\"]").Count > 0)
                {
                    price = htmlDoc.QuerySelectorAll("span[font-family=\"price\"]").First().InnerHtml;
                    if (price.IndexOf("class") != -1)
                    {
                        price = price.Substring(0, price.IndexOf("."));
                        price += ".";
                        price += htmlDoc.QuerySelectorAll("sup[font-family=\"price\"]").First().InnerHtml;
                    }
                }
                else
                {
                    price = "0.0";
                }

                if (htmlDoc.QuerySelectorAll("div.StrikeThrough__StyledStrikeThrough-sc-14w59iq-0 span.jneAgd").Count > 0)
                {
                    priceRegular = htmlDoc.QuerySelectorAll("div.StrikeThrough__StyledStrikeThrough-sc-14w59iq-0 span.jneAgd").First().InnerHtml;
                    if (priceRegular.IndexOf(">") != -1)
                    {
                        if (priceRegular.IndexOf(">") != -1)
                        {
                            priceRegular = priceRegular.Substring(0, priceRegular.IndexOf("."));
                        }
                        if (priceRegular.IndexOf(">") != -1)
                        {
                            priceRegular = priceRegular.Substring(priceRegular.IndexOf(">") + 1);
                        }
                        if (priceRegular.IndexOf(">") != -1)
                        {
                            priceRegular = priceRegular.Substring(priceRegular.IndexOf(">") + 1);
                        }
                        if (htmlDoc.QuerySelectorAll("sup[color=\"grey4\"]").Count > 0)
                        {
                            priceRegular += ".";
                            priceRegular += htmlDoc.QuerySelectorAll("sup[color=\"grey4\"]").First().InnerHtml;
                        }
                    }
                }
                
                string previewImage = "";

                List<string> images = new List<string>();

                IList<HtmlNode> nodes = htmlDoc.QuerySelectorAll("div.ZoomImage__StyledZoomImage-p1l8ru-0 source");

                string nodeSrc = "";
                foreach (HtmlNode node in nodes)
                {
                    nodeSrc = node.GetAttributeValue("srcset", "");

                    if (nodeSrc.Contains("?"))
                    {
                        nodeSrc = nodeSrc.Split(new string[] { "?" }, StringSplitOptions.None)[0];
                    }

                    if (nodeSrc.Contains("/skin/"))
                    {
                        continue;
                    }

                    if (previewImage.Length <= 0)
                    {
                        previewImage = nodeSrc;
                        break;
                    }

                    images.Add(nodeSrc);
                }

                IList<HtmlNode> nodes1 = htmlDoc.QuerySelectorAll("div.Gallerystyled__StyledCarouselThWrapper-asqw77-0  img");
                foreach (HtmlNode node in nodes1)
                {
                    nodeSrc = node.GetAttributeValue("src", "");

                    if (nodeSrc.Contains("?"))
                    {
                        nodeSrc = nodeSrc.Split(new string[] { "?" }, StringSplitOptions.None)[0];
                    }

                    if (nodeSrc.Contains("/skin/"))
                    {
                        continue;
                    }

                    if (nodeSrc == previewImage)
                    {
                        continue;
                    }

                    images.Add(nodeSrc);
                }

                if (images.Count <= 0 && htmlDoc.QuerySelectorAll("#productDataJson").Count > 0)
                {
                    string jsonString = htmlDoc.QuerySelectorAll("#productDataJson").First().InnerText;

                    JObject json = JObject.Parse(jsonString);

                    if (json.ContainsKey("variations"))
                    {
                        JToken token = json["variations"].First;

                        string[] t = json["variations"].ToString().Split(new string[] { "\"" }, 3, StringSplitOptions.None);
                        if (t.Length > 0)
                        {
                            string[] b = t[1].Split(new string[] { "\"" }, 3, StringSplitOptions.None);

                            if (b[0].Length > 0 && !b[0].Contains("\""))
                            {
                                int length = json["variations"][b[0]].ToString().Split(new string[] { "mainImage" }, StringSplitOptions.None).Length;
                                length = length > 0 ? length - 2 : 0;

                                for (int x = 0; x < length; x++)
                                {
                                    try
                                    {
                                        string img = "https://i.otto.de/i/otto/" + json["variations"][b[0]]["images"][x]["id"];
                                        Form1.getInstance().bLog("Bild von JSON: " + img);
                                        images.Add(img);
                                    }
                                    catch (Exception) { }
                                }
                            }
                        }
                    }
                }

                int imagesCount = images.Count;

                if (previewImage.Length > 0) imagesCount++;

                Produkt p = null;



                if (
                    htmlDoc.QuerySelectorAll("h1[itemprop=\"name\"]").Count > 0
                )
                {
                    if (Form1.priceFormat == "00")
                    {
                        if (priceRegular.Contains("."))
                        {
                            priceRegular = priceRegular.Split(new string[] { "." }, StringSplitOptions.None)[0] + ".00";
                        }
                        else
                        {
                            priceRegular = priceRegular + ".00";
                        }

                        if (price.Contains("."))
                        {
                            price = price.Split(new string[] { "." }, StringSplitOptions.None)[0] + ".00";
                        }
                        else
                        {
                            price = price + ".00";
                        }
                    }
                    else if (Form1.priceFormat == "99")
                    {
                        if (priceRegular.Contains("."))
                        {
                            priceRegular = priceRegular.Split(new string[] { "." }, StringSplitOptions.None)[0] + ".99";
                        }
                        else
                        {
                            priceRegular = priceRegular + ".99";
                        }

                        if (price.Contains("."))
                        {
                            price = price.Split(new string[] { "." }, StringSplitOptions.None)[0] + ".99";
                        }
                        else
                        {
                            price = price + ".99";
                        }
                    }

                    List<Review> reviews = new List<Review>();
                    IList<HtmlNode> reviewTemp = htmlDoc.QuerySelectorAll("div.fTOGgv div.Cardstyled__StyledCardWrapper-sc-137rc73-5");
                    foreach (HtmlNode node in reviewTemp)
                    {
                        String receiveTemp1 = node.InnerHtml;
                        var htmlDocReview = new HtmlAgilityPack.HtmlDocument();
                        htmlDocReview.LoadHtml(receiveTemp1);
                        String ReceiveName = htmlDocReview.QuerySelectorAll("span[itemprop=\"author\"]").First().InnerHtml;
                        String ReceiveTitle = htmlDocReview.QuerySelectorAll("p[itemprop=\"name\"]").First().InnerHtml;
                        String ReceiveDescription = htmlDocReview.QuerySelectorAll("p[itemprop=\"description\"]").First().InnerHtml;
                        String strStar = htmlDoc.QuerySelectorAll("span[itemProp=\"ratingValue\"]").First().InnerHtml;
                        int ReceiveStar = Int32.Parse(strStar.Substring(0, 1));
                        Review arrayReview = new Review(ReceiveName, ReceiveTitle, ReceiveDescription, ReceiveStar);
                        reviews.Add(arrayReview);
                    }

                    String stfff = HttpUtility.HtmlDecode(htmlDoc.QuerySelectorAll("h1.Typostyled__StyledInfoTypo-sc-5k7scz-0").First().InnerHtml);
                    String productName = HttpUtility.HtmlDecode(htmlDoc.QuerySelectorAll("h1.Typostyled__StyledInfoTypo-sc-5k7scz-0").First().InnerHtml);
                    string[] productWords = productName.Split(' ');
                    String descrition = "";
                    String strEAN = "";
                    int nEAN = html.IndexOf("ean");
                    if (nEAN == -1)
                    {
                        strEAN = "";
                    }
                    else
                    {
                        strEAN = html.Substring(nEAN + 6, 13);
                    }

                    try
                    {
                        descrition = HttpUtility.HtmlDecode(htmlDoc.QuerySelectorAll("div[itemprop=\"description\"]").First().InnerHtml);
                    }
                    catch (Exception ex)
                    {
                        descrition = "";
                    }

                    p = new Produkt()
                    {
                        Name = productName,
                        Image = previewImage,
                        Reviews = reviews,
                        Images = images,
                        ImagesCount = imagesCount,
                        Price = price,
                        PriceRegular = priceRegular,
                        Description = descrition,
                        EAN = strEAN,
                        Supplier = productWords[0],
                        Index = -1,
                        Sku = "A" + getCurrentUnix() + Form1.RandomString(4),
                        Category = ""
                    };

                    Form1.getInstance().bLog("Hinzugefügt: " + p.Name);
                }

                return p;
            }
            catch (Exception ex)
            {
                Form1.getInstance().bLog(ex);
            }

            return null;
        }

        public int getCurrentUnix()
        {
            return (Int32)(DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;
        }

        public List<string> GetAllCategoryPages(string categoryURL, int perPage)
        {
            List<string> urls = new List<string>();
            string url;

            for (int i = 0; i < 15; i++)
            {
                if (i == 0)
                {
                    urls.Add(categoryURL);
                    continue;
                }
                url = categoryURL + "?page=" + (i + 1);
                urls.Add(url);
            }

            return urls;
        }

        public override List<string> GetAllProductURLsFromCategoryURL(string categoryURL, int perPage)
        {
/*            ChromeOptions optionsMedia = new ChromeOptions();
            Proxy proxy = new Proxy();
            proxy.Kind = ProxyKind.Manual;
            proxy.IsAutoDetect = false;
        //    proxy.SslProxy = "51.81.69.12:5836";
            proxy.SslProxy = "158.101.98.173:3128";
            optionsMedia.Proxy = proxy;
            optionsMedia.AddArgument("ignore-certificate-errors");
            MediaDriver = new ChromeDriver(optionsMedia);*/
            List<string> urls = new List<string>();

            foreach (string cURL in this.GetAllCategoryPages(categoryURL, perPage))
            {
                foreach (string pURL in this.GetAllProductURLsFromCategoryPage(cURL))
                {
                    urls.Add(pURL);
                }
            }
            return urls;
        }

        public List<string> GetAllProductURLsFromCategoryPage(string categoryURL)
        {
            List<string> urls = new List<string>();

            var htmlDoc = new HtmlAgilityPack.HtmlDocument();


            return urls;
        }

        public override bool IsValidProduktURL(string url)
        {
            return
                url.ToLower().StartsWith("http://" + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("https://" + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("http://www." + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("https://www." + this.getDomain().ToLower());
        }

        public override bool IsValidCategoryURL(string url)
        {
            return
                url.ToLower().StartsWith("http://" + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("https://" + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("http://www." + this.getDomain().ToLower()) ||
                url.ToLower().StartsWith("https://www." + this.getDomain().ToLower());
        }
    }
}
