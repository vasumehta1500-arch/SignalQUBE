from analysis.drug_analysis import DrugAnalysis

analysis = DrugAnalysis()

drug_df = analysis.load_data()

top20 = analysis.top_drugs(drug_df)

print(top20)

analysis.create_chart(top20)