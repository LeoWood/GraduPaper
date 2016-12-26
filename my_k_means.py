import os
import random
from math import sqrt


docs_VecNorms = {}


def VecNorm(vec):
    return sqrt(sum([pow(v, 2) for k, v in vec.items()]))


def FileRead(dirname):
    docs_dict = {}
    for f in os.listdir(dirname):
        with open(dirname+'\\'+f, 'r', encoding='utf-8') as fr:
            words_dict = {}
            for line in fr.readlines():
                if line != '':
                    items = line.split('\t')
                    word = items[0].strip()
                    if len(word) < 2:
                        continue
                    w = float(items[1].strip())
                    words_dict[word] = w
            id = int(f[:-4])
            docs_dict[id] = words_dict
            docs_VecNorms[id] = VecNorm(words_dict)
    return docs_dict


def Distance(v1, VecNorm_v1, v2, VecNorm_v2):
    if VecNorm_v1 == 0 or VecNorm_v2 == 0:
        return 1.0
    mixed = 0
    for word, w in v1.items():
        if word in v2:
            mixed += w*v2[word]
    return 1.0-mixed/(VecNorm_v1*VecNorm_v2)


def VecRange(docs_dict):
    tokens = {}
    for id, words_dict in docs_dict.items():
        for word, w in words_dict.items():
            if word not in tokens:
                tokens[word] = []
            tokens[word].append(w)
    range_dict = {}
    for word, wlist in tokens.items():
        range_dict[word] = (min(wlist), max(wlist))
    return range_dict


def VecRandom(range_dict):
    random_vec = {}
    for word, range in range_dict.items():
        random_vec[word] = range[0]+(range[1]-range[0])*random.random()
    return random_vec


def ClustCenter(clust, docs_dict):
    center_vec = {}
    num = len(clust)
    for c in clust:
        for word, w in docs_dict[c].items():
            if not word in center_vec:
                center_vec[word] = 0.0
            center_vec[word] += w
    for word, w_sum in center_vec.items():
        center_vec[word] = w_sum/num
    return center_vec


def KCluster(docs_dict, k):
    range_dict = VecRange(docs_dict)
    centers = []
    for i in range(k):
        centers.append(VecRandom(range_dict))

    centers_VecNorm = []
    for i in range(k):
        centers_VecNorm.append(VecNorm(centers[i]))
    lastmatches = None

    for t in range(40):
        print('Iteration %d' % t)
        bestmatches = [[] for i in range(k)]

        for id in docs_dict.keys():
            doc = docs_dict[id]
            doc_VecNorm = docs_VecNorms[id]
            bestmatch = 0
            min_dis = 9999999
            for i in range(k):
                d = Distance(
                    doc, doc_VecNorm, centers[i], centers_VecNorm[i])
                if d < min_dis:
                    bestmatch = i
                    min_dis = d
            bestmatches[bestmatch].append(id)

        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

        for i in range(k):
            centers[i] = ClustCenter(bestmatches[i], docs_dict)

    return bestmatches


def Silhouette(clusters, docs_dict):
    Si = 0
    print(len(docs_dict))
    for clust in clusters:
        print(len(clust))
        for id in clust:
            xi = docs_dict[id]
            xi_norm = docs_VecNorms[id]
            d = 0
            for i in clust:
                if i != id:
                    d += Distance(xi, xi_norm, docs_dict[i], docs_VecNorms[i])
            ai = d/(len(clust)-1)
            dl = []
            for cl in clusters:
                if cl != clust:
                    d = 0
                    for j in cl:
                        d += Distance(xi, xi_norm,
                                      docs_dict[j], docs_VecNorms[j])
                    dl.append(d/len(cl))
            bi = min(dl)
            Si += (bi-ai)/max(ai, bi)
    return Si/len(docs_dict)


if __name__ == '__main__':
    corpus_dir = r'F:\毕业论文\test\test18046'
    docs_dict = FileRead(corpus_dir)
    print('create vectorspace')
    k = 100
    clusters = KCluster(docs_dict, k)
    fw = open('F:\\毕业论文\\test\\result18046\\'+str(k)+'(si).txt', 'w')
    for clust in clusters:
        fw.write('%s\n' % ','.join([str(id) for id in clust]))
    print('Cluster Done')
    Si = Silhouette(clusters, docs_dict)
    print('Silhouette Coefficient: '+str(Si))
