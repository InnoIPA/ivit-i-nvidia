import json

print_json = lambda data: [ print(info) for info in ['-'*50, json.dumps(data, indent=4)] ]

# Load json file
path = "/etc/docker/daemon.json"
with open(path, 'r') as f:
    data = json.load(f)
print('\nBefore:')
print_json(data)

# Modify data
key, val = 'default-runtime', 'nvidia'
if not key in data.keys():
    data.update( {key: val} )
else:
    if val != data[key]: data[key] = val

# Overwrite file
with open(path, 'w') as f:
    f.write(json.dumps(data))
print('\nAfter:')
print_json(data)

# Original
# --------------------------------------------------
# {
#     "runtimes": {
#         "nvidia": {
#             "path": "nvidia-container-runtime",
#             "runtimeArgs": []
#         }
#     }
# }

# Expect After
# --------------------------------------------------
# {
#     "runtimes": {
#         "nvidia": {
#             "path": "nvidia-container-runtime",
#             "runtimeArgs": []
#         }
#     },
#     "default-runtime": "nvidia" 
# }