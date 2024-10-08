Title: Mass export data from STATATLAS
Date: 2024-05-26
Modified: 2024-10-02
Slug: statatlas-export

![STATATLAS Thumbnail](../images/statatlas_thumbnail.png)

I find it difficult to compare different municipalities with eachother in Switzerland.
The Federal Statistical Office (BFS) does publish many data, but it is hard to collect various data from

* a) each municipality in Swizterland (location)
* b) over multiple years (time)
* c) over multiple indicators (scope)

The [STATATLAS (statistical atlas)](https://www.atlas.bfs.admin.ch/de/index.html) gives a great overview over various indicators, over time, for municipalities, regions or cantons.
This is exactly the data I searched for, because it allows a broad overview over the municipalities in Switzerland.
According to the BFS, there is currently no possibility to download all the STATATLAS data at once.
To download multiple yars for one indicator, I had to click on the download button for each year for this one indicator.

In this post I will explain how I downloaded all the data from STATATLAS in 3 different approaches:

* Approach 1: Use DAM-API to search for datasets related to STATATLAS
* Approach 2: Brute force download URL
* Approach 3: Use `structure.json`

## Approach 1: Use DAM-API to search for datasets related to STATATLAS

**Loaded rows**

2'134'923 (only municipalities)

**Links**

* [Python script](https://github.com/fbardos/homelab_elt/blob/main/homelab_airflow/dags/bfs_statatlas/run_bfs_statatlas.py)
* [Airflow DAG](https://github.com/fbardos/homelab_elt/blob/c98dbf5de5e235f5308f31ad69e531a9d50ae054/homelab_airflow/dags/bfs_statatlas/dag_bfs_statatlas.py)
* [Swagger DAM API](https://dam-api.bfs.admin.ch/hub/swagger-ui/index.html)

After asking the BFS, I got a hint: They have a [API called DAM-API](https://www.bfs.admin.ch/bfs/de/home/dienstleistungen/forschung/api/api-diffusion-dam.html), where the metadata of their data gets published.
And indeed, the data published on STATATLAS is also listed on this api:

```bash
curl --location --request GET 'https://dam-api.bfs.admin.ch/hub/api/dam/assets?articleModel=900052&spatialdivision=900004'
```

Whereas

* `articleModel=900052` stands for the STATATLAS product
* and `spatialdivision=900004` stands for data on municipality level

What was still missing is the data itself. By looking at the URL from the CSV download button, I got something like `https://www.atlas.bfs.admin.ch/core/projects/13/xshared/csv/26712_131.csv`, where `26712` is some kind of ID and `131` must stand for the selected language (when selecting French as language, I get `132`). When I can find this ID also in the DAM-API, I can mass download all indicators for all years on municipality level. In the field `shop.orderNr` i finally found then the reference between CSV name and the DAM-API.
That the data always comes in the same structure for all indicators on STATATLAS and years comes very handy, because I can now concat all dataframes over all indicators together with `pandas.concat`.

Columns of the exported CSV:
```bash
ipdb> df.columns
Index(['GEO_ID', 'GEO_NAME', 'VARIABLE', 'VALUE', 'UNIT', 'STATUS',
       'STATUS_DESC', 'DESC_VAL', 'PERIOD_REF', 'SOURCE', 'LAST_UPDATE',
       'GEOM_CODE', 'GEOM', 'GEOM_PERIOD', 'MAP_ID', 'MAP_URL'],
      dtype='object')
```

So, iterating over all indicators on municipality level and over all years on STATATLAS gives me the following dataset with **2.1 million rows**:

```bash
ipdb> df.info()
<class 'pandas.core.frame.DataFrame'>
Index: 2134923 entries, 0 to 4325
Data columns (total 16 columns):
 #   Column       Dtype  
---  ------       -----  
 0   GEO_ID       object 
 1   GEO_NAME     object 
 2   VARIABLE     object 
 3   VALUE        float64
 4   UNIT         object 
 5   STATUS       object 
 6   STATUS_DESC  object 
 7   DESC_VAL     object 
 8   PERIOD_REF   object 
 9   SOURCE       object 
 10  LAST_UPDATE  object 
 11  GEOM_CODE    object 
 12  GEOM         object 
 13  GEOM_PERIOD  object 
 14  MAP_ID       int64  
 15  MAP_URL      object 
dtypes: float64(1), int64(1), object(14)
memory usage: 276.9+ MB
```

This data can then loaded e.g. into a database to perform transformations and analysis downstream.

Cons:

* Some data is missing.

## Approach 2: Brute force download URL

**Loaded rows**

5'040'141 (all)

**Links**

* [Python script](https://github.com/fbardos/homelab_elt/blob/main/homelab_airflow/dags/bfs_statatlas/run_bfs_statatlas_iteration.py)
* [Airflow DAG](https://github.com/fbardos/homelab_elt/blob/main/homelab_airflow/dags/bfs_statatlas/dag_bfs_statatlas.py)

Unfortunately, I could not find all the maps displayed on STATATLAS also on DAM API with my first approach.
As an example, the map with the number of [inhabitants per municipality for year 2000](https://www.atlas.bfs.admin.ch/maps/13/de/74_72_71_70/12.html), I could not find on the DAM API.
But because the map IDs are kind ascending, I tried out to iterate over numbers between 0 and 30'000 to download the CSVs and concat them into one single dataframe:

```python
...
dataframes = []
for i in range(30_000):
    try:
        dataframes.append(pd.read_csv(f'https://www.atlas.bfs.admin.ch/core/projects/13/xshared/csv/{i}_131.csv', sep=';'))
    except urllib.error.HTTPError:
        continue
...
```

From approach 1, the highest map ID was 27642.

This is surely not an optimal solution, because...

* it sends a lot of requests to the backend from the BFS to download the data
* the duration of the task is significantly longer (70 vs. 7 minutes) than using the DAM API

## Approach 3: Use structure.json

**Loaded rows**

5'222'043 (all)

**Links**

* Dagster Asset: TODO

For some weeks, I continued to use approach 2. But I saw multiple new data with the same variable name for different variables.
One example:

* [STATATLAS: Amount of workers in Retail, 2022](https://www.atlas.bfs.admin.ch/maps/13/de/18030_9084_9075_138/27833.html)
* [STATATLAS: Amount of workers in Chemicals and Pharma, 2022](https://www.atlas.bfs.admin.ch/maps/13/de/18028_9080_9075_138/27829.html)

Both have the variable name `Anzahl Beschäftigte in Vollzeitäquivalenten` in their CSV exports.
I know, it is a bad idea to treat a variable string as ID, but it was the only possibility with the above approaches, when I want to combine multiple years together.

So I was looking for another solution. Also, because I was sending a lot of requests to the BFS.
When observing the network request during visiting one of the maps, I found some interesting JSON files:

```text
https://www.atlas.bfs.admin.ch/json/13/project.json
  Containing some information about the STATATLAS itself.

https://www.atlas.bfs.admin.ch/json/design/1.json
  Settings about the appearance of STATATLAS.

https://www.atlas.bfs.admin.ch/json/language/131.json
  Some translations in German.

https://www.atlas.bfs.admin.ch/json/projects.json
  Lists the BFS products which are included in STATATLAS.

https://www.atlas.bfs.admin.ch/json/13/patterns/<MAP_ID>.json
  Containing the hierarchy path of a map.

https://www.atlas.bfs.admin.ch/json/13/structures/<STRUCTURE_ID>.json          <---
  Lists the current hierarchy name (in DE and FR), its name and its children.
  When the hierarchy is deep enough, it will list the maps in the key `info`.
  The root structure is `STRUCTURE_ID = 2857`

https://www.atlas.bfs.admin.ch/json/13/maps/<MAP_ID>.json
  Information about a specific map for the presentation in STATATLAS.

https://www.atlas.bfs.admin.ch/json/13/labels/<GEO_REF>.json
  Labels for geographic areas like municipalities.

https://www.atlas.bfs.admin.ch/json/13/data/<MAP_ID>.json
  Containing the data of the map for the tabluar view in STATATLAS.
```

For me, the structures/ endpoint is interesting for me.
When recursively load all childrens, I could get all the maps referenced with the root and even get a structure of the topics to better distinguish indicators.
No need to brute force map IDs anymore.


