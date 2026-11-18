#pragma once
// NOCTURNE ring modulator: SPEED moves the sound to the sum and difference of the note and the carrier; DEPTH blends;
// its own ATTACK / DECAY bring the ring in and take it out over each note.
static bool ringModTests(){
 using namespace juce;
 auto require=[](bool ok,const char* what){if(!ok)std::cerr<<"RING: "<<what<<"\n";return ok;};
 auto render=[](std::initializer_list<std::pair<const char*,float>> settings){std::unique_ptr<AudioProcessor> p(createPluginFilter());p->setRateAndBufferSizeDetails(48000,256);p->prepareToPlay(48000,256);
  for(auto [id,v]:std::initializer_list<std::pair<const char*,float>>{{"reverbOn",0},{"delayOn",0},{"chorusMode",0},{"age",0},{"env",0},{"envB",0},{"cutoff",300}})if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));
  for(auto [id,v]:settings)if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));
  AudioBuffer<float> b(2,256),all(1,256*400);for(int i=0;i<400;++i){MidiBuffer m;if(i==0)m.addEvent(MidiMessage::noteOn(1,45,.8f),0);p->processBlock(b,m);all.copyFrom(0,i*256,b,0,0,256);}return all;};
 // rising zero crossings per second over [from, from + 0.2 s)
 auto rate=[](const AudioBuffer<float>& a,float fromSeconds){const int from=int(fromSeconds*48000.f);int n=0;for(int i=from+1;i<from+9600;++i)if(a.getSample(0,i-1)<0&&a.getSample(0,i)>=0)++n;return float(n)*5.f;};
 const auto dry=render({}),ringed=render({{"ringDepth",1},{"ringSpeed",1000}});
 if(!require(rate(dry,1.f)<200.f&&rate(ringed,1.f)>700.f,"full DEPTH moves the note up around the carrier"))return false;
 const auto decaying=render({{"ringDepth",1},{"ringSpeed",1000},{"ringDecay",2.f}});
 if(!require(rate(decaying,0.f)>700.f&&rate(decaying,1.85f)<200.f,"DECAY takes the ring out after the start of the note"))return false;
 const auto rising=render({{"ringDepth",1},{"ringSpeed",1000},{"ringAttack",1.2f}});
 if(!require(rate(rising,.0f)<200.f&&rate(rising,1.5f)>700.f,"ATTACK brings the ring in over the note"))return false;
 const auto keyed=render({{"ringDepth",1},{"ringSpeed",1000},{"ringKey",1}}); // KEY: 1000 Hz for middle C, so about 420 Hz on A2
 if(!require(rate(keyed,1.f)>300.f&&rate(keyed,1.f)<600.f,"KEY: the carrier follows the note"))return false;
 std::cout<<"PASS ring modulator: depth, speed, its own attack and decay, key follow ("<<rate(dry,1.f)<<" / "<<rate(ringed,1.f)<<" / "<<rate(keyed,1.f)<<" crossings/s)\n";return true;
}
