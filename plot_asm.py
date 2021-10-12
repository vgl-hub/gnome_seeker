#! /usr/bin/env python3.9

import pandas as pd
import plotly.express as px

"""
df = px.data.medals_long()
fig = px.scatter(df, y="nation", x="count", color="medal", symbol="medal")
fig.update_traces(marker_size=10)
fig.show()
fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
fig.show()
"""

df = pd.read_csv("final_tagged.tsv", sep='\t')
print(df.head())

fig = px.scatter(df, y="scaffold_n50", x="contig_n50", log_x=True,log_y=True,color="Taxon",hover_name="Organism",hover_data=["VGP_tag"])
fig.update_traces(marker_size=10)
fig.show()
fig.write_html("asm.html")