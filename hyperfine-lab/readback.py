import json

data = json.load(open("bench.json"))
print("schema", data["schema_version"], "| primary metric:", data["primary_metric"])
for r in data["results"]:
    t = r["summary"]["time_wall_clock"]
    m = r["summary"]["memory_peak_resident"]
    print(f"{r['name']}: {t['count']} runs, wall mean {t['mean']*1000:.2f} ms, "
          f"stddev {t['stddev']*1000:.2f} ms, median {t['median']*1000:.2f} ms, "
          f"peak memory mean {m['mean']/1048576:.1f} MiB")
