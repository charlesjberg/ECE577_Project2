%%
clear all
close all
CityTable = readtable("DistancesToMATowns.txt");
numTowns = ceil(sqrt(length(CityTable{:,1})))-1
bristolCountyTowns = [2 10 59 106 111 104 139 141 142 151 161 168 187 188 204 216 227 231];
numSearch = length(bristolCountyTowns);
%% Generate Initial Population
NewBedfordIndex = 128;
numChromosomes = 40;
for n = 1:numChromosomes
    randomVector = rand(1, numSearch-1);
%     cityVector = [1:NewBedfordIndex-1 NewBedfordIndex+1:numTowns];
    [a_sorted, a_order] = sort(randomVector);
    Route(n,:) = [NewBedfordIndex bristolCountyTowns(a_order) NewBedfordIndex];
end
%% Main Loop
numIterations = 1000;
numChildren = round(numChromosomes*.7);
numRandom = numChromosomes;
mutationProb = 1/(numSearch*5);
tic


 for i = 1:numIterations
     i
      Routes_Saved(i+1,:,:) = Route;
    [scores(i,:), bestScore(i), bestScoreIndex(i), populationFitness(i) scoreProb]  = fitness_test(CityTable, Route, "time");
     [vals, Routes_Ordered] = sort(scoreProb, 'descend');
   
    for n = 1:numRandom
        randomVector = rand(1, numSearch-1);
        cityVector = [1:NewBedfordIndex-1 NewBedfordIndex+1:numTowns];
        [a_sorted, a_order] = sort(randomVector);
        RouteRand(n,:) = [NewBedfordIndex bristolCountyTowns(a_order) NewBedfordIndex];
    end
      NextGen = [ RouteRand];
     Route = NextGen;
    bestScore(i)
 end
 timeElapsed = toc
%%
iterations = 1:i;
figure
plot(iterations, populationFitness)
ylabel("Total Population Score (sec)");
xlabel("Iteration")
title("Population Performance Improvement")
grid on

figure
plot(iterations, bestScore)
ylabel("Best Route Score (sec)");
xlabel("Iteration")
title("Best Route Performance Improvement")
grid on
%% Analysis - Find Average 
for i = 1:length(scores(:,1))
    for j = 1:length(scores(1,:))
    scores_ALL((i-1)*20+j) = scores(i,j);
    end
end
figure
histogram(scores_ALL, 30,'Normalization','probability');
xlabel("Score in Seconds of Route");
ylabel("Probability of Score")
title("PDF of Route Score TSP w/ 18 Cities")

scores_sigma = mean(scores_ALL) - std(scores_ALL).*[1:8];

%%
clear all; close all;
CityTable = readtable("DistancesToMATowns.txt");
sigma = 2485;
mean_score = 34954;
for numTrials = 1:100
    numTrials
numTowns = ceil(sqrt(length(CityTable{:,1})))-1;
bristolCountyTowns = [2 10 59 106 111 104 139 141 142 151 161 168 187 188 204 216 227 231];
numSearch = length(bristolCountyTowns);
% Generate Initial Population
NewBedfordIndex = 128;
numChromosomes = 20;
for n = 1:numChromosomes
    randomVector = rand(1, numSearch-1);
%     cityVector = [1:NewBedfordIndex-1 NewBedfordIndex+1:numTowns];
    [a_sorted, a_order] = sort(randomVector);
    Route(n,:) = [NewBedfordIndex bristolCountyTowns(a_order) NewBedfordIndex];
end
% Main Loop
numIterations =100;
numChildren = round(numChromosomes*.7);
numRandom = round(numChromosomes*.05);
mutationProb = 1/(numSearch*3);
bestRoutes(1,:) = zeros(1, length(Route(1,:)));
j=1;
 for i = 1:numIterations
      Routes_Saved(i+1,:,:) = Route;
    [scores(i,:), bestScore(i), bestScoreIndex(i), populationFitness(i) scoreProb]  = fitness_test(CityTable, Route, "time");
     indexesForBreeding = find_fittest(scoreProb, numChildren+1);
     Offspring = breed(Route, indexesForBreeding);
     [vals, Routes_Ordered] = sort(scoreProb, 'descend');
   
    for n = 1:numRandom
        randomVector = rand(1, numSearch-1);
        cityVector = [1:NewBedfordIndex-1 NewBedfordIndex+1:numTowns];
        [a_sorted, a_order] = sort(randomVector);
        RouteRand(n,:) = [NewBedfordIndex bristolCountyTowns(a_order) NewBedfordIndex];
    end
      NextGen = [Offspring; Route(Routes_Ordered(1:(numChromosomes - numChildren- numRandom)),:); RouteRand];
      [NextGen NumMutations(i,:)] = mutate(mutationProb, NextGen);
      best_Route = Route(Routes_Ordered(1),:);
      if (sum(best_Route(:) == bestRoutes(j,:)') < numSearch + 1)
          j = j + 1;
          bestRoutes(j,:) = best_Route;
      end
      
     Route = NextGen;
 end
 scoreTrial(numTrials) = min(bestScore);
end

sigmas_from_mean = (mean_score - scoreTrial)./sigma;
figure
histogram(sigmas_from_mean,6, 'Normalization','probability');
xlabel("Score \sigma from mean")
ylabel("Probability")
title("PDF of GA Best Route after 100 Iterations")