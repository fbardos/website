"""
I work with sdmx1, because the original pandasSDMX got not updated for 2 years
and throws errror when trying to import.

 - Pypi: https://pypi.org/project/sdmx1
 - Documentation sdmx1: https://sdmx1.readthedocs.io/

"""

import sdmx

# Define a custom SDMX source. The id can be read from
#   stats.swiss -> <select dataset> -> Entwickler-API
src_gws = {
    'id': 'CH1.GWS',
    'url': 'https://disseminate.stats.swiss/rest/',
    "name": "StatsSwiss GWS",
    "supports": {"codelist": False, "preview": True},
}
src = sdmx.add_source(src_gws, override=True)
client = sdmx.Client('CH1.GWS')


# METADATA ----------------------------------------------------------------------------

# Get information about the source dataflows
flow = client.dataflow()

# Get the different datasets as pandas.DataFrame
sdmx.to_pandas(flow.dataflow)

# Inspect on specific dataflow, returns the structure of a dataset itself.
flow.dataflow.DF_GWS_REG1

# Get the metadata structure for DF_GWS_REG1
meta = client.dataflow(resource=flow.dataflow.DF_GWS_REG1)

# Get the dimensions, attributes and measures for GWS_REG1
dims = meta.structure.get('DSD_GWS_REG1').dimensions.components
attrs = meta.structure.get('DSD_GWS_REG1').attributes.components
values = meta.structure.get('DSD_GWS_REG1').measures.components

# Get a single dimension
dim_gkats = meta.structure.get('DSD_GWS_REG1').dimensions.get('GKATS')

# Get the possible values of one single dimension
dim_gkats.local_representation.enumerated.items


# DATA --------------------------------------------------------------------------------
# Get data for Winterthur
sdmx.to_pandas(client.data('DF_GWS_REG1', key='A...230', params=dict(startPeriod=2010)))
