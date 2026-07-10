import pandas as pd
import re

# 1.My mock data input
raw_test_data = "10/07/2026, 15:30 - CC : Having sharp pelvic pain today.\n10/07/2026, 15:35 -  Bot: How long have you been experiencing this pain?"
print("--STEP 1 : RAW DATA --")
print (raw_test_data)

# 2. Testing pattern we broke down earlier
pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

# 3. See what re.split does
messages = re.split(pattern, raw_test_data)[1:]
print("\n--- STEP 2: SPLIT MESSAGES ---")
print(messages)

# 4. Let's see exactly what re.findall does
dates = re.findall(pattern, raw_test_data)
print("\n--- STEP 3: EXTRACT DATES ---")
print(dates)

# 5. Separate user from message
for message in messages:
    entry = re.split('([\w\W]+?):\s', message)
    print("Split result:", entry)

