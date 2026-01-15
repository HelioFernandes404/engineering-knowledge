import * as cheerio from 'cheerio';

export class Pizza {
    constructor(name: string, price: string) {
        this.name = name;
        this.price = price;
    }

    name: string;
    price: string;
}

async function GetPizzaListTheHtml(html: any) {
    let listPizza: Pizza[] = []


    const $ = cheerio.load(html);

    $('.oestabelecimento').each((index, element) => {
        const nomeProduto = $(element).find('div[align="left"] > b').first().text().trim();

        const precoProduto = $(element).find('#precotemp b').text().trim();


        listPizza.push(new Pizza(nomeProduto, precoProduto));
    });

    return listPizza;
}


async function GetContentPage() {
    try {
        const response = await fetch("https://peppersoftware.websiteseguro.com/lucaspizzaria/mostracardapio.php?c=PIZZAS%20SALGADAS&cs=PIZZAS%20SALGADAS");

        if (!response.ok) {
            return new Error()
        }

        const pageContent: string = await response.text();

        if (!pageContent) {
            return new Error("O conteudo esta vazio!")
        }

        return pageContent || "";
    } catch (e) {
        return new Error("Error ao obter o conteudo da site")
    }
}


async function Run() {
    const webSite = await GetContentPage();

    if (webSite instanceof Error) {
        return webSite;
    }

    let result = GetPizzaListTheHtml(webSite).then(pizzaList => {
        const result = pizzaList.filter(pizza => pizza.price === "R$ 34,99");
        console.log(result);
    }).catch(e => {
        return new Error("Error ao bucar as pizzas")
    })

    return true;
}

Run()


