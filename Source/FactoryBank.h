#pragma once
#include <juce_core/juce_core.h>
#include <FactoryData.h>

// NOCTURNE factory bank: the 40 factory sounds (Presets/Sounds) embedded in the binary, played by BANK A to E and
// PATCH 1-8 in the order below, so the program buttons give Nocturne's own sounds even before the installer ran.
class FactoryBank {
public:
 static const juce::StringArray& order() {
  static const juce::StringArray names{
   // A: brass that swells under the fingers
   "BRASS - Night Brass","BRASS - Pressure Swell","BRASS - Rising Octave","BRASS - Wah Horns",
   "BRASS - Low Section","BRASS - Bright Stabs","BRASS - Ribbon Fanfare","BRASS - Felt Horns",
   // B: crying pads and dark pads
   "PAD - Crying Strings","PAD - Weeping Choir","PAD - Dark Hall","PAD - Slow Tide",
   "PAD - Midnight Glass","PAD - Moon Drift","PAD - Sorrow Strings","PAD - Deep Velvet",
   // C: ring bells and keys
   "BELL - Ring Bells","BELL - Glass Chimes","BELL - Temple Gong","BELL - Ice Mallets",
   "KEYS - Felt Keys","KEYS - Ring Tremolo","KEYS - Dual Clav","KEYS - Silver Harpsi",
   // D: ribbon leads and basses
   "LEAD - Ribbon Solo","LEAD - Crying Lead","LEAD - Twin Saw","LEAD - Ring Lead",
   "BASS - Night Bass","BASS - Dual Pluck","BASS - Ring Bass","BASS - Velvet Low",
   // E: textures, effects, sequences (press PLAY) and chord memory
   "FX - Night Wind","FX - Metal Rain","FX - Rising Sweep","FX - Distant Sirens",
   "SEQ - Night Pulse","SEQ - Ring Steps","CHORD - Dark Minor","CHORD - Open Fifths"};
  return names;
 }
 static std::unique_ptr<juce::XmlElement> load(const juce::String& name) {
  for(int i=0;i<FactoryData::namedResourceListSize;++i)
   if(juce::String::fromUTF8(FactoryData::originalFilenames[i]).upToLastOccurrenceOf(".orbitpreset",false,false)==name){
    int size=0;const auto* data=FactoryData::getNamedResource(FactoryData::namedResourceList[i],size);
    return data?juce::XmlDocument::parse(juce::String::fromUTF8(data,size)):nullptr;}
  return {};
 }
};
