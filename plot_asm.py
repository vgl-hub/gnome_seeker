#! /usr/bin/env python3.9

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("final_tagged.tsv", sep='\t')
print(df.head())

df = df.sort_values(['Taxon', 'Project'])


hover_text = []
for index, row in df.iterrows():
    hover_text.append(('Organism: {Organism}<br>'+
                      'AssemblyAccession: {AssemblyAccession}<br>'+
                      'contig_n50: {contig_n50}<br>'+
                      'scaffold_n50: {scaffold_n50}<br>'+
                      'total_length: {total_length}<br>'+
                      'Source: {Project}<br>').format(Organism=row['Organism'],
                                            AssemblyAccession=row['AssemblyAccession'],
                                            contig_n50=row['contig_n50'],
                                            scaffold_n50=row['scaffold_n50'],
                                            total_length=row['total_length'],
                                            Project=row["Project"]
                                            ))

df["text"]=hover_text
global taxon_names
taxon_names=sorted(list(set(df.Taxon)))
taxon_data={taxon:df.query("Taxon == '%s'" %taxon) for taxon in taxon_names}


"""
aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
"""

fig = go.Figure()
colors=["lightgreen","red","cornflowerblue","darkgrey","mediumorchid","chocolate","forestgreen"]
for taxon_name, taxon in taxon_data.items():
	index_=taxon_names.index(taxon_name)
	fig.add_trace(go.Scatter(x=taxon["contig_n50"], y=taxon["scaffold_n50"], marker=dict(color=colors[index_]),mode='markers',name=taxon_name,marker_size=12,text=taxon['text']))

#fig.add_trace(go.Scatter(x=df["contig_n50"], y=df["scaffold_n50"],mode='markers',marker = dict(size=12, color=list(map(SetColor, df['Taxon'])))))


#fig.update_traces(mode='markers')
fig.add_vline(x=1000000, line_width=1, line_dash="dash", line_color="red")
fig.add_hline(y=10000000, line_width=1, line_dash="dash", line_color="red")
fig.update_traces(marker=dict(sizemode='area',  line=dict(width=1, color='white')),selector=dict(mode='markers'))
fig.update_layout(
    title='NCBI Vertebrate Genomes Contiguity',
    xaxis=dict(
        title='Contig N50',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='Scaffold N50',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    paper_bgcolor='aliceblue',#'rgb(243, 243, 243)',
    plot_bgcolor='aliceblue', #rgb(243, 243, 243)',
    #updatemenus=[
    #dict(type="buttons", direction="right",active=0,
    #buttons=list([
    #dict(method = "update", label="Taxa", args =[{"visible": [True, False]},{"title":"Taxa"}])
    #])
    #)
    #]
    )
"""
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
    updatemenus=[
        dict(
            type="buttons", direction="right",
            active=0,x = 11, y = 1.2,
            buttons=list(
                [
                    dict(
                        method = "update", label="Taxa", args =[{"visible": [True, False]},{"title":"Taxa"}],
                    ),
                    dict(
                        method = "update", label="Source", args =[{"visible": [True, False]},{"title":"Source"}],
                    ),
                ]
            ),
        )
    ]
)
"""

fig.write_html("asm.html")
fig.show()

"""
fig = px.scatter(df, y="scaffold_n50", x="contig_n50",log_x=True,log_y=True,color="Taxon",hover_name="Organism",hover_data=["Project","AssemblyAccession","total_length"])
fig.update_traces(marker_size=15,opacity=0.75)
fig.add_vline(x=1000000, line_width=2, line_dash="dash", line_color="red")
fig.add_hline(y=10000000, line_width=2, line_dash="dash", line_color="red")

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.7,
            y=1.2,
            showactive=True,
            buttons=list(
                [
                    dict(
                        label="AllP",
                        method="update",
                        args=[{"color": [df["Taxon"]]}],
                    ),
                    dict(
                        label="VGP",
                        method="update",
                        args=[{"color": [df["Project"]]}],
                    ),
                ]
            ),
        )
    ]
)


fig.show()
fig.write_html("asm.html")
"""