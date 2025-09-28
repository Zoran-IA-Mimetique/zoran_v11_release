run:
	python -m glyphnet_ultimate_v2.run_pipeline config/pipelines/full_proof_of_value_suite.yaml

test:
	pytest -q
