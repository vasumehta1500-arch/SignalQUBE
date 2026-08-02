from analysis.signal_detection import SignalDetector

detector = SignalDetector()

pairs = detector.top_drug_reaction_pairs(10)

print("\nTop Drug-Reaction Pairs\n")
print(pairs)

drug = pairs.iloc[0]["drugname"]
reaction = pairs.iloc[0]["pt"]

print("\nCalculating Signal...\n")

result = detector.calculate_signal(drug, reaction)

print(result)