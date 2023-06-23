import requests
import json

baseurl = 'https://api.stat-trading.tech'
headers: dict = {"Content-Type": "application/json"}

changeObj = {
    "fromDate": "2018-01-01",
    "toDate": "2023-05-27",
    # "abstype": 1,
    "script": "NIFTY",
    "timeFrame": "daily"
}

changeData: dict = json.loads(requests.post(
    f"{baseurl}/price/consecutivedays", json=changeObj, headers=headers).text)

# scripts: dict = json.loads(requests.get(
#     f"{baseurl}/scripts/allScripts",  headers=headers).text)

scripts = [{
    "id": 195,
    "name": "NIFTY",
    "zerodha_code": "256265"
    },
    {
    "id": 196,
    "name": "NIFTYBANK",
    "zerodha_code": "260105"
    }]

analyticsDict: dict = {
    "green": {},
    "red": {},
    }
for script in scripts:
    script_name = script["name"]
    changeObj["script"] = script_name
    changeData: dict = json.loads(requests.post(
        f"{baseurl}/price/consecutivedays", json=changeObj, headers=headers).text)
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    curr = 0
    next = 0

    green_extremePercent = 0.4
    red_extremePercent = 1.0
    
    print(script_name)
    for i in range(len(changeData)-1):
        curr = changeData[i]["net"]
        next = changeData[i+1]["net"]
        nextGap = changeData[i+1]["gap"]
        if ((curr >= 0.0 and next >= -0.2) or (curr < 0.0 and next <= 0.2)):
            count1 += 1

        curr = changeData[i]["intra"]
        next = changeData[i+1]["intra"]
        if ((curr >= 0.0 and changeData[i+1]["netHigh"] >= 0.4) or (curr <= 0.0 and changeData[i+1]["netLow"] <= -0.4)):
            count2 += 1
        
        # Calculate w.r.t. to high's and lows
        curr = changeData[i]["net"]
        next = changeData[i+1]["net"]
        if ((curr >= 0.0 and changeData[i+1]["netHigh"] >= green_extremePercent) or (curr < 0.0 and changeData[i+1]["netLow"] <= -1*green_extremePercent)):
            count3 += 1
        
        # Gap Analysys Green
        if ((curr >= 0.0 and nextGap >= 0.4) or (curr < 0.0 and nextGap <= -0.4)):
            count4 += 1

    analyticsDict["green"][script_name] = {
        "net": count1/(len(changeData)-1),
        "intra": count2/(len(changeData)-1),
        "netExtremes": count3/(len(changeData)-1),
        "gapAnalysys": count4/(len(changeData)-1)
    }
    # For the red Days    
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0

    for i in range(len(changeData)-1):
        curr = changeData[i]["net"]
        next = changeData[i+1]["net"]
        nextGap = changeData[i+1]["gap"]
        if ((curr >= 0.0 and next <= -0.4) or (curr < 0.0 and next >= 0.4)):
            count1 += 1

        curr = changeData[i]["net"]
        if ((curr >= 0.0 and changeData[i+1]["netLow"] <= -1*red_extremePercent) or (curr > 0.0 and changeData[i+1]["netHigh"] >= red_extremePercent)):
            count3 += 1

        # Gap Analysys Green
        if ((curr >= 0.0 and nextGap <= -1.0 ) or (curr < 0.0 and next >= 1.0)):
            count4 += 1
            # Gap Analysys Green
        if ((curr >= 0.0 and nextGap <= -1.0 and changeData[i+1]["netHigh"] >= -0.2) or (curr < 0.0 and next >= 1.0 and changeData[i+1]["netLow"] <= 0.2)):
            count5 += 1
    
    analyticsDict["red"][script_name] = {
        "net": count1/(len(changeData)-1),
        "netExtremes": count3/(len(changeData)-1),
        "gapAnalysys": count4/(len(changeData)-1),
    }
    
    analyticsDict["info"] = [
        f"GREEN Extreme percent: {green_extremePercent}%",
        f"RED Extreme percent: {red_extremePercent}%",
        ]
with open(f'output/result_{green_extremePercent}.json', 'w') as outfile:
    json.dump(analyticsDict, outfile, indent=4)
    outfile.close()
