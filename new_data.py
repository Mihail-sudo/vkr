from numpy import pi


c_1 = [0.5, 0.9, 0.9]
a_1 = (0, 0, 0)
m_1 = [[1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1]]


## ggg
c_2 = [0.9, 0.5, 0.9]
a_2 = (-pi / 180 * 114, pi / 180 * 118, pi / 180 * 74)
m_2 = [[0.95101216, 0.08088845, -0.29838387, -1.84195694],
       [-0.05955586, 0.99502042, 0.07992158, 0.80679145],
       [0.30336278, -0.05823589, 0.9510939, 0.48082126],
       [0.,          0.,          0.,          1.        ]]


c_3 = [0.3, 0.7, 0.5]
a_3 = (-pi / 180 * 118, -pi / 180 * 132, -pi / 180 * 82)
m_3 = [[0.99512023,  0.04634417,  0.08710886,  1.25746576],
       [-0.05835564,  0.98831102,  0.14084013,  1.30770764],
       [-0.07956353, -0.14523615,  0.98619273, 1-0.1198768 ],
       [ 0.,          0.,          0.,          1.        ]]


c_4 = [0.5, 0.3, 0.9]
a_4 = (-pi / 180 * 90, -pi / 180 * 180, 0)
m_4 = [[ 9.99366966e-01,  3.55757178e-02,  1.86982661e-04, 0.139],
       [-3.53886341e-02,  9.94623090e-01, -9.73270385e-02, 0.985],
       [-3.64845653e-03,  9.72588102e-02,  9.95252437e-01, 1.405],
       [ 0.,  0.,  0.,  1.]]


colors = [c_1, c_2, c_3, c_4]
angles = [a_1, a_2, a_3, a_4]
matrixes = [m_1, m_2, m_3, m_4]
