# from processing.nlm_processing.query_engine import (
#     create_engines,
#     create_llm,
#     create_query_tools,
# )


# def create_router(tools: list, llm):
#     return RouterQueryEngine.from_defaults(
#         query_engine_tools=tools, llm=llm, select_multi=False, verbose=True
#     )


# def build_query_router(frames: dict):
#     llm = create_llm()
#     engines = create_engines(frames, llm)
#     tools = create_query_tools(engines)
#     return create_router(tools, llm)
