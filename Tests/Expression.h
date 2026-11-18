#pragma once
// NOCTURNE expression: per-key pressure (polyphonic aftertouch) shapes only the key pressed; the ribbon bends the pitch.
static bool expressionTests(){
 using namespace juce;
 auto require=[](bool ok,const char* what){if(!ok)std::cerr<<"EXPRESSION: "<<what<<"\n";return ok;};
 auto make=[](std::initializer_list<std::pair<const char*,float>> settings){auto* p=createPluginFilter();p->setRateAndBufferSizeDetails(48000,256);p->prepareToPlay(48000,256);
  for(auto [id,v]:std::initializer_list<std::pair<const char*,float>>{{"reverbOn",0},{"delayOn",0},{"chorusMode",0},{"age",0},{"env",0},{"envB",0},{"lfoAmount",0}})if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));
  for(auto [id,v]:settings)if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));return std::unique_ptr<AudioProcessor>(p);};
 auto run=[](AudioProcessor& p,int blocks,std::function<void(int,MidiBuffer&)> events){AudioBuffer<float> b(2,256),all(2,256*blocks);
  for(int i=0;i<blocks;++i){MidiBuffer m;events(i,m);p.processBlock(b,m);for(int c=0;c<2;++c)all.copyFrom(c,i*256,b,c,0,256);}return all;};
 // Per key: with SPREAD PITCH the low key sits on one side, the high key on the other; pressing only one key harder
 // (PRESSURE > AMP) must move the stereo balance toward that key's side, and the other key's side must not swell.
 auto balanceShift=[&](int pressedNote){auto p=make({{"voiceSpread",1},{"voiceWidth",1},{"atVolume",1}});
  auto a=run(*p,160,[&](int i,MidiBuffer& m){if(i==0){m.addEvent(MidiMessage::noteOn(1,40,.8f),0);m.addEvent(MidiMessage::noteOn(1,88,.8f),0);}
   if(i>=80)m.addEvent(MidiMessage::aftertouchChange(1,pressedNote,127),0);});
  auto ratio=[&](int from){return a.getRMSLevel(0,from,256*30)/jmax(1e-9f,a.getRMSLevel(1,from,256*30));};
  return ratio(256*120)/jmax(1e-9f,ratio(256*40));};
 const float low=balanceShift(40),high=balanceShift(88);
 if(!require((low>1.08f&&high<.93f)||(low<.93f&&high>1.08f),"polyphonic pressure on one key shapes only that key"))return false;
 // RIBBON: half the strip to the right with RANGE 12 lifts the note by six semitones (frequency x 1.414).
 auto pitchOf=[&](float ribbon){auto p=make({{"cutoff",2000},{"ribbonRange",3},{"ribbon",ribbon}});
  auto a=run(*p,120,[&](int i,MidiBuffer& m){if(i==0)m.addEvent(MidiMessage::noteOn(1,45,.8f),0);});
  int crossings=0;for(int i=256*40+1;i<256*110;++i)if(a.getSample(0,i-1)<0&&a.getSample(0,i)>=0)++crossings;return float(crossings);};
 const float centre=pitchOf(0),bent=pitchOf(.5f);
 if(!require(std::abs(bent/jmax(1.f,centre)-1.4142f)<.06f,"the ribbon bends the pitch by its range"))return false;
 std::cout<<"PASS expression: per-key pressure ("<<low<<" / "<<high<<"), ribbon +6 st ("<<centre<<" > "<<bent<<" crossings)\n";return true;
}
