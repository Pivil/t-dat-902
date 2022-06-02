import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from webcolors import (
    CSS2_HEX_TO_NAMES,
    hex_to_rgb,
)


class ColorService:
    def get_palette(self, clusters):
        width=300
        image_palette = np.zeros((50, width, 3), np.uint8)
        steps = width/clusters.cluster_centers_.shape[0]
        for idx, centers in enumerate(clusters.cluster_centers_):
            image_palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
        return image_palette
    def get_color_values(self, colors):
        res = []
        l = colors[0].tolist()
        for i in range(len(l)):
            if l[i] in res:
                continue
            else:
                res.append(l[i])
        return res
    def get_kmean_cluster(self, n, image):
        clt = KMeans(n_clusters=n)
        return clt.fit(image.reshape(-1, 3))

    def test(self):
        print('aa')
    def convert_rgb_to_names(self, rgb_tuple):
        # a dictionary of all the hex and their respective names in css3
        css3_db = CSS2_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]

    def get_n_width_palette(self, n, image):
        clt = self.get_kmean_cluster(n, image)
        return self.get_palette(clt)

