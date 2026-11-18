#pragma once
// NOCTURNE dual layers: two separate chains per voice, each with its own filter and envelopes; the levelled filter envelope.
static bool dualLayerTests(){
 using namespace juce;
 auto require=[](bool ok,const char* what){if(!ok)std::cerr<<"DUAL: "<<what<<"\n";return ok;};
 {poly8test::Contour c;c.setSampleRate(48000);c.setParameters({.05f,.2f,.3f,.1f,.3f,1.f});c.noteOn();const float first=c.getNextSample();float atPeak=0;for(int i=0;i<2400;++i)atPeak=jmax(atPeak,c.getNextSample());
  float settled=0;for(int i=0;i<48000;++i)settled=c.getNextSample();
  if(!require(std::abs(first-.3f)<.02f&&atPeak>.97f&&std::abs(settled-.3f)<.02f,"levelled envelope: I.L, up to A.L, back to I.L"))return false;}
 auto render=[](std::initializer_list<std::pair<const char*,float>> settings){std::unique_ptr<AudioProcessor> p(createPluginFilter());p->setRateAndBufferSizeDetails(48000,256);p->prepareToPlay(48000,256);
  for(auto [id,v]:std::initializer_list<std::pair<const char*,float>>{{"reverbOn",0},{"delayOn",0},{"chorusMode",0},{"age",0},{"dualLayer",1},{"env",0},{"envB",0},{"cutoff",300},{"cutoffB",9000},{"filterBType",1}})if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));
  for(auto [id,v]:settings)if(auto* r=dynamic_cast<RangedAudioParameter*>(parameterOf(*p,id)))r->setValueNotifyingHost(r->convertTo0to1(v));
  AudioBuffer<float> b(2,256),all(1,256*120);for(int i=0;i<120;++i){MidiBuffer m;if(i==0)m.addEvent(MidiMessage::noteOn(1,57,.8f),0);p->processBlock(b,m);all.copyFrom(0,i*256,b,0,0,256);}return all;};
 auto bright=[](const AudioBuffer<float>& a,int from,int to){double d=0,l=0;for(int i=from+1;i<to;++i){const float x=a.getSample(0,i),y=a.getSample(0,i-1);d+=(x-y)*(x-y);l+=x*x;}return d/jmax(l,1e-12);};
 const auto one=render({{"oscLayer",0}}),two=render({{"oscLayer",1}});
 if(!require(bright(two,12000,30000)>bright(one,12000,30000)*4,"layer II goes through its own (open) filter, layer I through its (closed) one"))return false;
 const auto slow=render({{"oscLayer",1},{"attack2",1.5f}});
 if(!require(slow.getRMSLevel(0,0,4800)<slow.getRMSLevel(0,25000,4800)*.4f,"layer II has its own amp envelope"))return false;
 std::cout<<"PASS dual layers: levelled filter envelope, separate filters per layer, separate amp envelope for layer II\n";return true;
}
