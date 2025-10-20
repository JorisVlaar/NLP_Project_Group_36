import ast
import pandas as pd

def filter_compound_tags(gamePath="comp/tagGamesDF.csv",
                         savePath="comp/tagGamesNoCompoundDF.csv",
                         compoundPath="compound_tags.csv"):
    # --- Load data ---
    tagGamesDF = pd.read_csv(gamePath)
    compounds = pd.read_csv(compoundPath)

    # Parse compound tags and lowercase
    compounds['tags_list'] = compounds['Compounds'].apply(lambda s: [t.lower() for t in ast.literal_eval(s)])
    compound_map = dict(zip(compounds['Compound tag'].str.lower(), compounds['tags_list']))

    # Expand tags
    def expand_tags(tag_str):
        expanded = []
        for t in ast.literal_eval(tag_str):
            expanded.extend(compound_map.get(t.lower(), [t.lower()]))
        return expanded

    tagGamesDF['tags'] = tagGamesDF['tags'].apply(expand_tags)

    # Save to CSV
    tagGamesDF.to_csv(savePath, index=False)

filter_compound_tags()
