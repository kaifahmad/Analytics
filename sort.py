import json

with open('output/result_0.5.json') as f:
  data = json.load(f)["green"]
  f.close()
# print(data)  
sorted_footballers_by_goals = sorted(data.items(), key=lambda x:x[1]["intra"])
with open('intra.json', 'w') as outfile:
    json.dump(sorted_footballers_by_goals, outfile,indent=4)
    outfile.close()

sorted_footballers_by_goals = sorted(data.items(), key=lambda x:x[1]["net"])
with open('net.json', 'w') as outfile:
    json.dump(sorted_footballers_by_goals, outfile,indent=4)
    outfile.close()

sorted_footballers_by_goals = sorted(data.items(), key=lambda x:x[1]["netExtremes"])
with open('netExtremes.json', 'w') as outfile:
    json.dump(sorted_footballers_by_goals, outfile,indent=4)
    outfile.close()    