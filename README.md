# 3D-Plane_Segmentation-Python
This will take a point cloud and find the planes. Region growing method finds the kxk neighborhood of points to find the normals, classifies like normals in the same planes. RANSAC methods chose a random set of points and find planes by pass a threshold for the number of inlier points per that choice.
