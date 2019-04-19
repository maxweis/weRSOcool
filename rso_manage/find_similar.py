import pandas as pd
import numpy as np
from .models import RSO, Tag
from .forms import COLLEGES



def get_vectors():
    tag_list = set()
    # vectors is map from rso_name -> feature vector
    vectors = {}
    for tag in Tag.objects.all():
        if tag.rso.name not in vectors:
            vectors[tag.rso.name] = set()
        tag_list.add(tag.tag.lower())
        vectors[tag.rso.name].add(tag.tag.lower())
    tag_list = list(tag_list)

    # turns the feature vectors from a set into an array
    for vec in vectors:
        vectors[vec] = [int(tag in vectors[vec]) for tag in tag_list]

    list_df = []
    for name, vec in vectors.items():
        college_name = RSO.objects.get(name=name).college_association

        college_vect = [int(college_name == temp_name) for temp_name in COLLEGES]
        tags = [x for x in vec]
        list_df.append(college_vect + tags + [name])
    df = pd.DataFrame(list_df)
    return df

def dist(v1, v2):
    v1 = (v1.values).tolist()[0]
    v2 = (v2.values).tolist()[0]
    if (len(v1) != len(v2)):
        return len(max(len(v1), len(v2))) * 100
    total = 0
    for i in range(len(v1)):
        if i < len(COLLEGES):
            total += abs((v1[i]) - (v2[i])) * 2
        else:
            if v1[i] and v2[i]:
                total -= 1
            else:
                total += abs(v1[i] - v2[i])
    return total

# Finds the rso that is most similar to the rso
def nearest(rso):
    closest = None
    df = get_vectors()
    try:
        x = df[df.columns[0:-1]]
        y = df[df.columns[-1]]
    except:
        return None

    index = -1
    if (rso.name not in y.tolist()):
        return None

    index = y.tolist().index(rso.name)
    if (index == -1):
        return None

    rso_tuple = x.iloc[[index]]

    min_dist = len(y) * 100
    for i in range(len(y)):
        distance = dist(rso_tuple, x.iloc[[i]])
        if y[i] != rso.name:
            if distance < min_dist:
                min_dist = distance
                closest = y[i]

    return closest
