import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from module.data import process_data
from module.model import inference


app = FastAPI()
[encoder, lb, model] = pickle.load(open("model/model.pkl", "rb"))
cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]


class CensusInputData(BaseModel):
    age: int
    workclass: str
    fnlgt: int
    education: str
    education_num: int = Field(alias='education-num')
    marital_status: str = Field(alias='marital-status')
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int = Field(alias='capital-gain')
    capital_loss: int = Field(alias='capital-loss')
    hours_per_week: int = Field(alias='hours-per-week')
    native_country: str = Field(alias='native-country')

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "age": 23,
                    "workclass": "Self-emp-not-inc",
                    "fnlgt": 8071,
                    "education": "HS-grad",
                    "education-num": 9,
                    "marital-status": "Married-civ-spouse",
                    "occupation": "Exec-managerial",
                    "relationship": "Husband",
                    "race": "White",
                    "sex": "Male",
                    "capital-gain": 0,
                    "capital-loss": 0,
                    "hours-per-week": 45,
                    "native-country": "United-States",
                },
            ]
        }
    }


@app.get("/")
def welcome_root():
    return {"message": "Welcome to the vnk8071 project!"}


@app.post(path="/infer")
async def prediction(input_data: CensusInputData):
    """
    Example function for returning model output from POST request.
    The function take in a single web form entry and converts it to a single
    row of input data conforming to the constraints of the features used in the model.
    Args:
        input_data (BasicInputData) : Instance of a BasicInputData object. Collected data from
        web form submission.
    Returns:
        dict: Dictionary containing the model output.
    """
    input_df = pd.DataFrame(
        {k: v for k, v in input_data.dict(by_alias=True).items()}, index=[0]
    )

    processed_input_data, _, _, _ = process_data(
        X=input_df,
        categorical_features=cat_features,
        label=None,
        training=False,
        encoder=encoder,
        lb=lb
    )

    prediction = inference(model, processed_input_data)
    return {"Output": ">50K" if int(prediction[0]) == 1 else "<=50K"}
