from sklearn.neighbors import KNeighborsClassifier
from .models import RSO, Tag

def get_vectors():
    tag_list = set()
    vectors = {}
    for tag in Tag.objects.all():
        if tag.rso.name not in vectors:
            vectors[tag.rso.name] = set()

        tag_list.add(tag.tag)
        vectors[tag.rso.name].add(tag.tag)

    tag_list = list(tag_list)

    for vec in vectors:
        vectors[vec] = [int(tag in vectors[vec]) for tag in tag_list]
    return vectors

# def dist(v1, v2):
#     total = 0
#     for x, y in zip(v1, v2):
#         total += (x - y) ** 2
#     return total
#
# # Finds the rso that is most similar to the rso
# def nearest(rso):
#     vectors = get_vectors()
#     if rso.name not in vectors:
#         return None
#     rso_vec = vectors[rso.name]
#
#     closest = None
#     min_dist = -1
#     for name, vec in vectors.items():
#         if (min_dist == -1 or dist(vec, rso_vec) < min_dist) and name != rso.name:
#             min_dist = dist(vec, rso_vec)
#             closest = name
#
#     return closest

def nearest(rso):
    vectors = get_vectors()
    keys, values = [], []
    for name, vec in vectors.items():
        if name != rso.name:
            vec_norm = vec.copy()
            for i in range(len(vec_norm)):
                # normalize vector
                vec_norm[i] /= sum(vec)
            vectors[name] = vec_norm
            keys.append(name)
            values.append(vec_norm)

    n = min(len(keys), 5)
    classifier = KNeighborsClassifier(n_neighbors=n, algorithm='kd_tree')
    classifier.fit(values, keys)
    y_pred = classifier.predict([vectors[rso.name],])
    return y_pred[0]
