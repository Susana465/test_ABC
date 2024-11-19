import mcell as m 

model = m.Model()

# Specify that this model uses BNG units
model.config.use_bngl_units = True

# Load information on species and reaction rules from BNGL file
model.load_bngl('ABC.bngl')

# Initialize simulation state
model.initialize()

# Simulate 10 iterations
model.run_iterations(10)

# Final simulation step
model.end_simulation()


