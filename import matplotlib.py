
import matplotlib.pyplot as plt
import numpy as np

# Example material properties (replace with actual data)
E_HA = 100 GPa  # Young's modulus of hydroxyapatite
E_CLG = 1 GPa    # Young's modulus of collagen
V_HA = np.linspace(0, 1, 100)  # Volume fraction of hydroxyapatite

# Calculate Voigt and Reuss bounds
E_Voigt = V_HA * E_HA + (1 - V_HA) * E_CLG
E_Reuss = 1 / (V_HA / E_HA + (1 - V_HA) / E_CLG)

# Example Young's moduli for compact bone, dentin, and enamel
Youngs_Moduli = {
    'Compact Bone': 15 GPa,
    'Dentin': 18 GPa,
    'Enamel': 85 GPa
}

# Plot Voigt and Reuss bounds and Young's moduli
plt.plot(V_HA, E_Voigt, label='Voigt Bound')
plt.plot(V_HA, E_Reuss, label='Reuss Bound')

for material, modulus in Youngs_Moduli.items():
    plt.axhline(y=modulus, color='gray', linestyle='--', label=material)

plt.xlabel('Volume Fraction of Hydroxyapatite')
plt.ylabel('Young\'s Modulus (GPa)')
plt.legend()
plt.title('Composite Bounds vs. Material Properties')
plt.grid(True)
plt.show()
