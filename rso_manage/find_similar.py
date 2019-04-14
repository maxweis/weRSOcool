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
        tag_list.add(tag.tag)
        vectors[tag.rso.name].add(tag.tag)
    tag_list = list(tag_list)

    # turns the feature vectors from a set into an array
    for vec in vectors:
        vectors[vec] = [int(tag in vectors[vec]) for tag in tag_list]

    list_df = []
    for name, vec in vectors.items():
        college_name = RSO.objects.get(name=name).college_association
        college_vect = [0] * len(COLLEGES)
        for i in range(len(COLLEGES)):
            if college_name == COLLEGES[i]:
                college_vect[i] = 1
        tags = []
        for num in vec:
            tags.append(num)
        list_df.append(college_vect + tags + [name])
    df = pd.DataFrame(list_df)
    return df

def dist(v1, v2):
    if (len(v1) != len(v2)):
        return len(max(len(v1), len(v2))) * 100
    total = 0
    for i in range(len(v1)):
        if i < len(COLLEGES):
            total += (int(v1[i]) - int(v2[i])) * 2
        else:
            total += (int(v1[i]) - int(v2[i]))
    return total

# Finds the rso that is most similar to the rso
def nearest(rso):
    df = get_vectors()
    x = df[df.columns[0:len(df.columns)-1]]
    y = df[len(df.columns)-1]

    index = -1
    index = y.tolist().index(rso.name)
    rso_tuple = x.iloc[[index]]

    min_dist = len(y) * 100
    for i in range(len(y)):
        distance = dist(rso_tuple, x.iloc[[index]])
        if y[i] != rso.name:
            if distance < min_dist:
                min_dist = distance
                closest = y[i]

    return closest
