import numpy as np
from sklearn.cluster import KMeans

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

    def get_n_width_palette(self, n, image):
        clt = self.get_kmean_cluster(n, image)
        return self.get_palette(clt)

    def draw_n_palette_width(self, n, image):
        clt = self.get_kmean_cluster(n, image)
        self.draw_image(self.get_palette(clt))
