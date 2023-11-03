def algo_chooser(query):
    from app.models.enums.algoChoice import AlgoChoice

    # from app.models.query import Query
    from app.models.enums.queryOperation import QueryOperation
    from typing import List

    print(query)

    if query.operation == QueryOperation.SELECT:
        for filter in query.filters:
            possible_plans: List[AlgoChoice] = []
            best_plan: AlgoChoice = None

            filter.possible_plans = possible_plans
            filter.best_plan = best_plan

    elif query.operation == QueryOperation.JOIN:
        print("join")
        pass

    print(query)
    return query
