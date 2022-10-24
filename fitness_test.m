function [scores, bestScore,  bestScoreIndex, populationFitness, scoreProb] = fitness_test(CityTable, routes, metric)
numTowns = ceil(sqrt(length(CityTable{:,1})))-1;
if (strcmp(metric, "time"))
    table_column = 4;
else
    table_column = 3;
end

scores = zeros(1, length(routes(:,1)));
for i = 1:length(routes(:,1))
    for j = 2:length(routes(1,:))
        fromCity = routes(i,j-1)-1;
        toCity = routes(i,j);
        if toCity > fromCity
            toCity = toCity - 1;
        end
        table_index = fromCity*243 + toCity;
        scores(i) = scores(i) + CityTable{table_index, table_column};
    end
end

    [bestScore bestScoreIndex] = min(scores);
    populationFitness = sum(scores);
    scoreProb = populationFitness./scores./(sum(populationFitness./scores));
    
end