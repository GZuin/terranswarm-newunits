#include "CommanderAgent.h"
#include <BWAPI.h>
#include <iostream>
#include <unordered_map>
#include <vector>
#include "Task.h"
#include "TaskAssociation.h"
#include <random>
#include <iostream>
#include "GeneticValues.h"
#include "Parameters.h"

using namespace BWAPI;
using namespace Filter;

CommanderAgent::CommanderAgent() : latencyFrames(10){
	_barracks.clear();
	_factories.clear();
	_commandCenters.clear();
}


CommanderAgent::~CommanderAgent(){

}

void CommanderAgent::onFrame(unordered_map<TaskType, vector<Task>*> tasklist, unordered_map<Unit, float> trainSCVIncentives) {

	map<int, double>& parameters = GeneticValues::getMap();
	
	for(unordered_map<Unit, float>::iterator iter = trainSCVIncentives.begin(); iter != trainSCVIncentives.end(); ++iter){
		Unit u =  iter->first;
		float incentive = iter->second;
		//double uniformOn01 = dis(gen);
		Task scv = Task(TrainWorker, iter->second);//&tasklist[TrainWorker]->at(0);
		TaskAssociation trainSCV = TaskAssociation(&scv, parameters[K_GENERAL_TRAIN_SCV]);
		//Broodwar->drawTextMap(u->getPosition(),"SCV inc: %.3f, T: %.3f", trainSCV.task()->getIncentive(), trainSCV.tValue());
	}

	//only acts every 'X' frames (X = latencyFrames)
	if (Broodwar->getFrameCount() % latencyFrames != 0){
		return;
	}

	//also does nothing if there is no supply or minerals available
	int supplyDiff = max(0, (Broodwar->self()->supplyTotal() - Broodwar->self()->supplyUsed())/2);
	if (supplyDiff == 0 || Broodwar->self()->minerals() < 50) return;

	
	std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(0, 1);

	for(unordered_map<Unit, float>::iterator iter = trainSCVIncentives.begin(); iter != trainSCVIncentives.end(); ++iter){
		Unit u =  iter->first;
		float incentive = iter->second;
		//double uniformOn01 = dis(gen);
		Task scv = Task(TrainWorker, iter->second);//&tasklist[TrainWorker]->at(0);
		TaskAssociation trainSCV = TaskAssociation(&scv, parameters[K_GENERAL_TRAIN_SCV]);

		//Broodwar->drawTextMap(u->getPosition(),"SCV inc: %.3f, T: %.3f", trainSCV.task()->getIncentive(), trainSCV.tValue());

		if( (rand() / float(RAND_MAX)) < trainSCV.tValue()){

		//if(uniformOn01 <= incentive){
			if ( u->getType().isResourceDepot() ) {
				// Order the depot to construct more workers! But only when it is idle.
				if ( u->isIdle() && !u->train(u->getType().getRace().getWorker()) ) {
					Error lastErr = Broodwar->getLastError();
					if(lastErr == Errors::Insufficient_Supply){
						//Broodwar->sendText("SVC can't be created - %s", lastErr.toString().c_str());	
						//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
					}
				} // closure: failed to train idle unit
			}
		}
	}

	//iterates through the barracks
	TaskAssociation trainMarine = TaskAssociation(&tasklist[TrainMarine]->at(0), parameters[K_GENERAL_TRAIN_MARINE]);
	TaskAssociation trainFirebat = TaskAssociation(&tasklist[TrainFirebat]->at(0), parameters[K_GENERAL_TRAIN_FIREBAT]);
	TaskAssociation trainGoliath = TaskAssociation(&tasklist[TrainGoliath]->at(0), parameters[K_GENERAL_TRAIN_GOLIATH]);
	TaskAssociation trainVulture = TaskAssociation(&tasklist[TrainVulture]->at(0), parameters[K_GENERAL_TRAIN_VULTURE]);
	TaskAssociation trainMedic = TaskAssociation(&tasklist[TrainMedic]->at(0), parameters[K_GENERAL_TRAIN_MEDIC]);
	Unitset myUnits = Broodwar->self()->getUnits();
	for ( Unitset::iterator u = myUnits.begin(); u != myUnits.end(); ++u ) {
		
		
		if ( u->getType() == UnitTypes::Terran_Barracks ) {
			
			if ((rand() / float(RAND_MAX)) < trainMedic.tValue() && u->isIdle() && !u->train(UnitTypes::Terran_Medic)) {
				Error lastErr = Broodwar->getLastError();
				if(lastErr == Errors::Insufficient_Supply){
					//Broodwar->sendText("Marine can't be created - %s", lastErr.toString().c_str());	
					//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
				}			
			}
			else if ((rand() / float(RAND_MAX)) < trainFirebat.tValue() && u->isIdle() && !u->train(UnitTypes::Terran_Firebat)) {
				Error lastErr = Broodwar->getLastError();
				if(lastErr == Errors::Insufficient_Supply){
					//Broodwar->sendText("Marine can't be created - %s", lastErr.toString().c_str());	
					//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
				}			
			}
			else if ((rand() / float(RAND_MAX)) < trainMarine.tValue() && u->isIdle() && !u->train(UnitTypes::Terran_Marine)) {
				Error lastErr = Broodwar->getLastError();
				if(lastErr == Errors::Insufficient_Supply){
					//Broodwar->sendText("Marine can't be created - %s", lastErr.toString().c_str());	
					//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
				}			
			}
		} //closure
		
		if ( u->getType() == UnitTypes::Terran_Factory ) {
			
			if ((rand() / float(RAND_MAX)) < trainVulture.tValue() && u->isIdle() && !u->train(UnitTypes::Terran_Vulture)) {
				Error lastErr = Broodwar->getLastError();
				if(lastErr == Errors::Insufficient_Supply){
					//Broodwar->sendText("Marine can't be created - %s", lastErr.toString().c_str());	
					//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
				}			
			}
			else if ((rand() / float(RAND_MAX)) < trainGoliath.tValue() && u->isIdle() && !u->train(UnitTypes::Terran_Goliath)) {
				Error lastErr = Broodwar->getLastError();
				if(lastErr == Errors::Insufficient_Supply){
					//Broodwar->sendText("Marine can't be created - %s", lastErr.toString().c_str());	
					//CommanderAgent::createSupply(Broodwar->getUnit(u->getID()));
				}			
			}
		}
	}
	
	TaskAssociation researchAcademyLongRange = TaskAssociation(&tasklist[ResearchAcademyLongRange]->at(0), .7f); //was[TrainMarine]
	if ((rand() / float(RAND_MAX)) < researchAcademyLongRange.tValue()){
		Broodwar << "Resquest U_238 upgrade" << endl;
		researchRequest(UpgradeTypes::U_238_Shells);
	}

	TaskAssociation researchAcademyStimPack = TaskAssociation(&tasklist[ResearchAcademyStimPack]->at(0), .7f);
	if ((rand() / float(RAND_MAX)) < researchAcademyStimPack.tValue()){
		Broodwar << "Resquest Stim Pack upgrade" << endl;
		researchRequest(TechTypes::Stim_Packs);
	}

	TaskAssociation researchArmoryWeapon = TaskAssociation(&tasklist[ResearchArmoryWeapon]->at(0), .7f); //was[TrainMarine]
	if ((rand() / float(RAND_MAX)) < researchArmoryWeapon.tValue()){
		Broodwar << "Resquest Vehicle Weapons upgrade" << endl;
		researchRequest(UpgradeTypes::Terran_Vehicle_Weapons);
	}

	TaskAssociation researchArmoryPlating = TaskAssociation(&tasklist[ResearchArmoryPlating]->at(0), .7f); //was[TrainMarine]
	if ((rand() / float(RAND_MAX)) < researchArmoryPlating.tValue()){
		Broodwar << "Resquest Vehicle Plating upgrade" << endl;
		researchRequest(UpgradeTypes::Terran_Vehicle_Plating);
	}
}

void CommanderAgent::createSupply(Unit u){
	Position pos = u->getPosition();
	Error lastErr = Broodwar->getLastError();
	Broodwar->registerEvent([pos, lastErr](Game*){ Broodwar->drawTextMap(pos, "%c%s", Text::White, lastErr.c_str()); },   // action
		nullptr,    // condition
		Broodwar->getLatencyFrames());
	
	UnitType supplyProviderType = u->getType().getRace().getSupplyProvider();
	static int lastChecked = 0;

	// If we are supply blocked and haven't tried constructing more recently
	if (  lastErr == Errors::Insufficient_Supply && lastChecked + 400 < Broodwar->getFrameCount() && Broodwar->self()->incompleteUnitCount(supplyProviderType) == 0 ) {

			lastChecked = Broodwar->getFrameCount();

			// Retrieve a unit that is capable of constructing the supply needed
			Unit supplyBuilder = u->getClosestUnit(  GetType == supplyProviderType.whatBuilds().first &&
				(IsIdle || IsGatheringMinerals) &&
				IsOwned);
			// If a unit was found
			if ( supplyBuilder ){

				if ( supplyProviderType.isBuilding() ){

					TilePosition targetBuildLocation = Broodwar->getBuildLocation(supplyProviderType, supplyBuilder->getTilePosition());
					if ( targetBuildLocation ){

						// Register an event that draws the target build location
						Broodwar->registerEvent([targetBuildLocation,supplyProviderType](Game*)
						{
							Broodwar->drawBoxMap( Position(targetBuildLocation),
								Position(targetBuildLocation + supplyProviderType.tileSize()),
								Colors::Blue);
						},
							nullptr,  // condition
							supplyProviderType.buildTime() + 100 );  // frames to run

						// Order the builder to construct the supply structure
						supplyBuilder->build( supplyProviderType, targetBuildLocation );
					}
				}
				else {
					// Train the supply provider (Overlord) if the provider is not a structure
					supplyBuilder->train( supplyProviderType );
				}
			} // closure: supplyBuilder is valid
	} // closure: insufficient supply
}

/**
  * Finds which building researches the required tech and researches it
  */
void CommanderAgent::researchRequest(TechType techType){
	if (!Broodwar->self()->hasResearched(techType) && !Broodwar->self()->isResearching(techType)) {
		Unitset units = Broodwar->self()->getUnits();
		
		for (Unitset::iterator unit = units.begin(); unit != units.end(); unit++){
			if(unit->getType() == techType.whatResearches() && unit->exists()){
				unit->research(techType);
			}
		}
	}
}

/**
  * Finds which building researches the required upgrade and researches it
  */
void CommanderAgent::researchRequest(UpgradeType upgdType){
	
	if (Broodwar->self()->getUpgradeLevel(upgdType) <= 0 && !Broodwar->self()->isUpgrading(upgdType)) {
		Unitset units = Broodwar->self()->getUnits();

		for (Unitset::iterator unit = units.begin(); unit != units.end(); unit++){
			if(unit->getType() == upgdType.whatUpgrades() && unit->exists()){
				unit->upgrade(upgdType);
			}
		}
	}
}
