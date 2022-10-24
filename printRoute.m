function printRoute(best_route, CityTable)
fileID = fopen('FinalRoute.txt','w');
for i = 1:length(best_route)
    table_index = (best_route(i)-1)*243 + 1;
    fprintf(fileID, char(CityTable{table_index,1}));
    fprintf(fileID, " \n");
end
