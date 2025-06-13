from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
import pandas as pd


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PATH = '/app/data/'

legislators = pd.read_csv(PATH + 'legislators.csv', encoding='utf-8')
bills = pd.read_csv(PATH + 'bills.csv', encoding='utf-8')
votes = pd.read_csv(PATH + 'votes.csv', encoding='utf-8')
vote_results = pd.read_csv(PATH + 'vote_results.csv', encoding='utf-8')

@app.get('/')
async def welcome():
    return "Welcome to our Bill Support Analyzer API"

@app.get('/support/by_legislator')
async def by_legislator():
    try:
        votes_by_legislator = vote_results.groupby(['legislator_id', 'vote_type']).size().unstack(fill_value=0)
        votes_by_legislator.columns = ['yea', 'nay']
        results_q1 = pd.merge(legislators[['id', 'name']], votes_by_legislator, left_on='id', right_index=True,
                              how='left')
        results_q1.fillna(0, inplace=True)

        return JSONResponse(content=jsonable_encoder(results_q1), status_code=HTTPStatus.OK)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while trying to list by Legislator {e}"
        )

@app.get('/support/by_bill')
async def by_bill():
    try:
        votes_by_bill = vote_results.groupby(['vote_id', 'vote_type']).size().unstack(fill_value=0)
        votes_by_bill.columns = ['supported', 'opposed']
        results_q2 = pd.merge(bills[['id', 'title', 'sponsor_id']], votes_by_bill, left_on='id', right_index=True,
                              how='left')
        results_q2.fillna(0, inplace=True)

        results_q2 = pd.merge(results_q2, legislators[['id', 'name']], left_on='sponsor_id', right_on='id', how='left')
        results_q2.rename(columns={'name': 'primary_sponsor'}, inplace=True)

        return JSONResponse(content=jsonable_encoder(results_q2), status_code=HTTPStatus.OK)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while trying to list by Bill {e}"
        )