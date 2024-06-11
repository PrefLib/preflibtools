from interval import is_WSC
from test_interval import generate_CEI_instances
import time

for i in range(272, 2000):
    start = time.time()
    print("Size:", i)
    instance = generate_CEI_instances(i, i)
    res = is_WSC(instance)
    end = time.time()
    print("Duration:", end - start)
    print(res)

    # Gebleven bij 272