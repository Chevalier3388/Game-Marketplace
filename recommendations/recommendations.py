# recommendations/recommendations.py

from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    GameCategory,
    GameRecommendation,
    RecommendationResponse,
)

import recommendations_pb2_grpc


games_by_category = {
    GameCategory.CLASSIC: [
        GameRecommendation(id=1, title="Шахматы"),
        GameRecommendation(id=2, title="Шашки"),
        GameRecommendation(id=3, title="Города"),
    ],

    GameCategory.CARD_GAMES: [
        GameRecommendation(
            id=4, title="1000"
        ),
        GameRecommendation(id=5, title="Канаста"),
        GameRecommendation(id=6, title="Дурак"),
    ],

    GameCategory.DUELING: [
         GameRecommendation(
            id=7, title="Анмачт"
        ),

        GameRecommendation(
            id=8, title="Андерворлд"
        ),

        GameRecommendation(id=9, title="Регард"),
    ],
}


class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):

    def Recommend(self, request, context):
        if request.category not in games_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        games_for_category = games_by_category[request.category]
        num_results = min(request.max_results, len(games_for_category))
        games_to_recommend = random.sample(
            games_for_category, num_results
        )

        return RecommendationResponse(recommendations=games_to_recommend)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()