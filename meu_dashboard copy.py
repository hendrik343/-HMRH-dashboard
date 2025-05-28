import pandas as pd
import matplotlib.pyplot as plt

# Lê o ficheiro Excel (tem de estar na mesma pasta!)
df = pd.read_excel("Dashboard_HSE_Completo.xlsx", sheet_name="Registo Diário")

# Mostra as primeiras linhas para confirmar
print(df.head())

# Exemplo: Gráfico de Acidentes por Hospital
acidentes = df.groupby("Hospital")["Nº Acidentes"].sum()
acidentes.plot(kind="bar", color="orange", title="Acidentes por Hospital")
plt.ylabel("Nº de Acidentes")
plt.xlabel("Hospital")
plt.show()
