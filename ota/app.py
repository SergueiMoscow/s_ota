from fastapi import FastAPI

from ota import views

app = FastAPI(docs_url='/')

origins = ['*']


@app.on_event('startup')
async def start():
    """
    Собрать поступившие релизы ???
    :return:
    """
    pass


app.include_router(views.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8079)
