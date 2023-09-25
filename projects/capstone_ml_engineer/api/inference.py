import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

try:
    from predicting.inference import input_fn, predict_fn, model_fn
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from predicting.inference import input_fn, predict_fn, model_fn

app = FastAPI()


class StrokeInput(BaseModel):
    id: int
    gender: str
    age: int
    hypertension: int
    heart_disease: int
    ever_married: str
    work_type: str
    Residence_type: str
    avg_glucose_level: float
    bmi: float
    smoking_status: str


@app.get("/")
def read_root():
    return {"Message": "Stroke Prediction API"}


@app.post("/predict")
def predict(request: StrokeInput):
    model = model_fn(model_dir="models/")
    input_data = input_fn(request_body=request)
    output_data = predict_fn(input_object=input_data, model=model)
    return {"Output": output_data}


if __name__ == "__main__":
    uvicorn.run(app="inference:app", host="0.0.0.0", port=8000, reload=True)
