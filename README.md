<a name="readme-top"></a>
# 📚 Table of Contents
- [ℹ About The Project](#about)
- [🌇 List of Collected Residential Projects](#projects) 
- [🛢Database](#db)
- [🔑Setup](#setup)
- [📊 Visualization](#viz)
- [🌐 API](#api) 
- [🌲 Project tree](#tree)
- [📄 License](#license)

<a name="about"></a>
<!-- ABOUT THE PROJECT -->
# ℹ️ About The Project

This project deploys a containerized AWS Lambda function, built using the Scrapy framework, to handle web scraping of various developer investments. The scraped data is stored in Google BigQuery for further analysis and reporting. Bash scripts are used to build and upload the Docker image to the AWS repository.

The project plans to gather a large number of developer investments over an extended period to analyze market trends.
Each time a new developer investment is added, a Bash script will be used to build and push a new containerized function to the AWS repository, allowing AWS Lambda to execute it seamlessly.

The collected data will be stored in Google BigQuery, visualized for insights, and shared via an API for broader accessibility.

## 👨‍💻 Built with

| Technology | Usage |
| ---------- | ------|
| <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>  | Used as the main programming language to develop and manage the Scrapy spiders.|
| <img src="https://repository-images.githubusercontent.com/529502/dab2bd00-0ed2-11eb-8588-5e10679ace4d" width="120" height="40"/>| Framework for building web scraping spiders to extract real estate data from websites.|
| <img src="https://img.shields.io/badge/bash_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white"/> | Scripts used to build Docker images and upload them to an AWS repository.|
| <img src="https://expandapis.com/wp-content/uploads/2024/04/aws-lambda.png" width="140" height="60"/> | Executes serverless functions to manage the scraping process dynamically.|
| <img src="https://img.shields.io/badge/Google Big Query-%234285F4?style=for-the-badge&logo=googlebigquery&logoColor=white"/>| 	Stores the scraped data for further analysis and reporting.|
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<a name="projects"></a>
<!-- LIST OF COLLECTED RESIDENTIAL PROJECTS -->
# 🌇 List of Collected Residential Projects

| ID  | Name                             | Developer Name | City | District | Start Date* | End Date* | url |
|-----|----------------------------------|----------------|------|----------|-------------|-----------|-----|
|  1  | Kolej na 19   |Polski Holding Nieruchomości   | Warszawa| Wola   | 01-02-2025   |  10-03-2025* |[Kolej na 19](https://kolejna19.pl/)   |
|  2  | Modern Mokotów   |Archicom  | Warszawa| Mokotów   | 01-02-2025   |   |[Modern Mokotów](https://modernmokotow.archicom.pl/)    |
|  3  | Stacja Wola   |Archicom  | Warszawa| Wola   | 01-02-2025   |   |[Stacja Wola](https://stacjawola.archicom.pl/)    |
|  4  | Żelazna 54   |Matexi Polska  | Warszawa| Wola   | 01-02-2025   |   |[Żelazna 54](https://matexipolska.pl/warszawa/zelazna-54)    |
|  5  | Murapol Urcity   |Murapol  | Warszawa| Ursus   | 09-02-2025   |   |[Murapol Urcity](https://murapol.pl/oferta/warszawa/murapol-urcity)    |
|  6  | Dom Hygge Twin   |Dynamic Development  | Warszawa| Mokotów   | 09-02-2025   |   |[Dom Hygge Twin](https://hyggemokotow.pl/)    |
|  7  | Oval Sky   |Dekpol  | Warszawa| Wola   | 14-02-2025   |   |[Oval Sky](https://dekpoldeweloper.pl/portfolio/ovalsky-warszawa-ul-pradzynskiego/?)   |
|  8  | Stilla   |Skanska  | Warszawa| Mokotów   | 14-02-2025   | 24-02-2025*  |[Stilla](https://mieszkaj.skanska.pl/nasze-projekty/stilla/)    |
|  9  | Chmielna Duo   |bpi  | Warszawa| Śródmieście   | 15-02-2025   |   |[Chmielna Duo](https://chmielnaduo.pl/)    |
|  10 | Park Skandynawia  |Skanska  | Warszawa| Praga-Południe   | 15-02-2025   |   |[Park Skandynawia](https://mieszkaj.skanska.pl/nasze-projekty/park-skandynawia/)    |
|  11 | Sadyba Spot   |unidevelopment  | Warszawa| Mokotów   | 15-02-2025   |   |[Sadyba Spot](https://sadybaspot.pl/)    |
|  12 | Bukowinska Mokotow   |Matexi Polska  | Warszawa| Mokotów   | 19-06-2025   |   |[Bukowińska Mokotów](https://matexipolska.pl/warszawa/bukowinska-mokotow)    |
|  13 | Hi Mokotow   |Cordia  | Warszawa| Mokotów   | 25-06-2025   |   |[Bukowińska Mokotów](https://cordiapolska.pl/inwestycje/hi-mokotow/)    |
|  14 | Łopuszańska 47   |SGI  | Warszawa| Włochy   | 26-06-2025   |   |[Łopuszańska 47](https://www.sgi.pl/warszawa/lopuszanska-47/)    |
|  15 | Senza  |Marvipol | Warszawa| Białoęka   | 28-06-2025   |   |[Senza](https://marvipol.pl/osiedle-senza/)    |
|  16 | Sengera  |Marvipol | Warszawa| Ursynów   | 02-07-2025   |   |[Sengera](https://marvipol.pl/sengera-1/)    |
|  17 | XYZ Place  |Matexi Polska | Warszawa| Włochy   | 07-07-2025   |   |[XYZ-Place](https://matexipolska.pl/warszawa/xyz-place)    |
|  18 | Zakątek Harmonia  |Atal | Warszawa| Białołęka   | 10-08-2025   |   |[Zakątek Harmonia](https://zakatekharmonia.pl/)    |
|  19 | Osiedle Poematu  |Atal | Warszawa| Wawer   | 12-08-2025   |   |[Osiedle Poematu](https://osiedlepoematu.pl)    |

The Start Date and End Date refer to the period during which the data was collected, not the actual start or end of the sales process.

* Finished scaraping earlier because of unadrressed technical difficulties

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="db"></a>
<!-- DATABASE -->
# 🛢 Database

| column_name | type |
| ----------- |------|
| date | TIMESTAMP |
| developer_name | STRING |
| flat_area | FLOAT |
| flat_available | INTEGER |
| flat_details_url | STRING |
| flat_floor | STRING |
| flat_name | STRING |
| flat_price | FLOAT |
| flat_price_per_sqm | FLOAT |
| flat_promotion | INTEGER |
| flat_rooms | STRING |
| investment_name | STRING |
| investment_url | STRING |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="setup"></a>
<!-- SETUP -->
# 🔑 Setup

## Local setup
Steps necessary to setup function.<br><br>
**Adjust .json key filename in pipelines.py** <br>
**Remember that your local image name has to be equal to repository name.**
```
git clone <repository_url>
cd image
```
Update AWS configuration variables
```
IMAGE_NAME=
AWS_REGION=
AWS_ACCOUNT=
```


Open Bash Terminal
```
bash image_update.sh
```
## AWS configuration

1. Create AWS repository & AWS Lambda function, video below:<br>
[![Watch on YouTube](https://img.youtube.com/vi/XES3gXg13KE/0.jpg)](https://youtu.be/XES3gXg13KE?si=jA_Ay0IE1NN1GJTb&t=576)

2. In AWS Lambda configuration setup Memory to be 512 MB & Timeout 5 minutes, default timeout value is 3 seconds and it makes function break.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="viz"></a>
<!-- VISUALIZATION -->
# 📊 Visualization 

Cooming soon

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="api"></a>
<!-- API -->
# 🌐 API 

Cooming soon

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="tree"></a>
<!-- PROJECT TREE -->
# 🌲 Project tree

```bash
.
├─── image
│    ├── Dockerfile
│    ├── image_update.sh    
│    ├── requirements.txt
│    └─── source
│         ├── __init__.py
│         ├── main.py #run spiders
│         ├── real-estate-tracker-437718-4857741a8e36.json #put our gcp key here
│         ├── scrapy.cfg
│         └── real_estate_prices
│             ├── __init__.py
│             ├── items.py
│             ├── middlewares.py
│             ├── pipelines.py
│             ├── settings.py
│             └── spiders
│                 ├── __init__.py
│                 ├── bukowinska_mokotow.py
│                 ├── chmielna_duo.py
│                 ├── dom_hygge_twin.py
│                 ├── hi_mokotow.py
│                 ├── kolej_na_19.py
│                 ├── lopuszanska_47.py
│                 ├── modern_mokotow.py
│                 ├── murapol_urcity.py
│                 ├── osiedle_poematu.py
│                 ├── oval_sky.py
│                 ├── park_skandynawia.py
│                 ├── sadyba_spot.py
│                 ├── sengera.py
│                 ├── senza.py
│                 ├── stacja_wola.py
│                 ├── stilla.py
│                 ├── xyz_place.py
│                 ├── zakatek_harmonia.py
│                 └── zelazna_54.py                
├── images
├── .gitignore 
├── README.md 
└── license.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a name="license"></a>
<!-- LICENSEE -->
# 📄 License

Distributed under the MIT License. See LICENSE.txt for more information.