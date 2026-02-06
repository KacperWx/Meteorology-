# ------------------ Define city data --------------------

def schina():
    dot_lons_schina = [114.1694, 113.5439, 113.2644,
                       113.0816, 111.9826, 110.9100,
                       110.3546, 110.3470, 109.1170,
                       108.3610,]
    dot_lats_schina = [22.3193, 22.1987, 23.1291,
                       22.5786, 21.8583, 21.6600,
                       21.2842, 20.0400, 21.4700,
                       21.6180,]
    dot_labels_schina = ['Hong Kong', 'Macau', 'Guangzhou',
                         'Jiangmen', 'Yangjiang', 'Maoming',
                         'Zhanjiang', 'Haikou', 'Beihai',
                         'Fangchenggang',]
    return dot_lons_schina, dot_lats_schina, dot_labels_schina

def echina():
    dot_lons_echina = [120.6993, 121.4274, 121.5503,
                       120.1551, 121.4737,
                       120.5853, 120.3119, 119.9737,
                       118.7969, 120.1614,
                       117.2272, 114.3054]

    dot_lats_echina = [28.0038, 28.6564, 29.8746,
                       29.8746, 31.2304,
                       31.2989, 31.4912, 31.8158,
                       32.0603, 33.3853,
                       31.8206, 30.5928]

    dot_labels_echina = ['Wenzhou', 'Taizhou', 'Ningbo',
                         'Hangzhou', 'Shanghai', 'Suzhou',
                         'Wuxi', 'Changzhou', 'Nanjing',
                         'Yancheng', 'Hefei', 'Wuhan',]
    return dot_lons_echina, dot_lats_echina, dot_labels_echina

def nvietnam():
    dot_lons_nvietnam = [105.8342, 106.6881, 106.1697, 105.7852]
    dot_lats_nvietnam = [21.0278, 20.8449, 20.4389, 19.8067]
    dot_labels_nvietnam = ['Hanoi', 'Haiphong', 'Nam Dinh', 'Thanh Hoa']
    return dot_lons_nvietnam, dot_lats_nvietnam, dot_labels_nvietnam

def laos():
    dot_lons_laos = [102.6331, 103.1856, 104.0479, 102.1387]
    dot_lats_laos = [17.9757, 19.4521, 20.4171, 19.8833]
    dot_labels_laos = ['Vientiane', 'Phonsavan', 'Sam Nuea', 'Luang Prabang']
    return dot_lons_laos, dot_lats_laos, dot_labels_laos

def ryukyus():
    dot_lons_ryukyus = [124.1556, 125.3247, 127.6785, 129.4938,]
    dot_lats_ryukyus = [24.3407, 24.7674, 26.2130, 28.3774,]
    dot_labels_ryukyus = ['Ishigaki', 'Miaykojima', 'Naha', 'Amami']
    return dot_lons_ryukyus, dot_lats_ryukyus, dot_labels_ryukyus

def sph():
    dot_lons_sph = [
        125.3958, # Davao
        124.6472, # Cagayan de Oro
        125.1716, # Dadiangas (General Santos)
        123.3072, # Dumaguete
        122.5667, # Iloilo City
        123.8854, # Cebu City
        118.7471, # Puerto Princesa
        119.3892  # El Nido
    ]

    dot_lats_sph = [
        7.2075,  # Davao
        8.4822,  # Cagayan de Oro
        6.1069,  # Dadiangas (General Santos)
        9.3068,  # Dumaguete
        10.7202, # Iloilo City
        10.3157, # Cebu City
        9.7392,  # Puerto Princesa
        11.1761  # El Nido
    ]

    dot_labels_sph = [
        'Davao', 'Cagayan de Oro', 'Dadiangas', 'Dumaguete',
        'Iloilo City', 'Cebu City', 'Puerto Princesa', 'El Nido'
    ]

    return dot_lons_sph, dot_lats_sph, dot_labels_sph