function printRoute(best_route, CityTable)
fileID = fopen('Results\FinalRoute.csv','w');
numCities = length(best_route(1,:));
numRoutes = length(best_route(:,1)); 
for j = 2:numRoutes
for i = 1:numCities
    table_index = (best_route(j,i)-1)*243 + 1;
    fprintf(fileID, char(CityTable{table_index,1}))
    fprintf(fileID, ",%i",best_route(j,i))
    fprintf(fileID, append(",", num2str(numCities)));
    fprintf(fileID, append(",", num2str(numRoutes-1)));
    fprintf(fileID, " \n");
end
end