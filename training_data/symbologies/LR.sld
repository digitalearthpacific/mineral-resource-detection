<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0" xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>lulc_masked_MaxEnt_nadi_2023</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="ramp">
              <sld:ColorMapEntry quantity="50.367424011230469" label="50.3674" color="#fff5f0"/>
              <sld:ColorMapEntry quantity="56.804672470092775" label="56.8047" color="#fee0d2"/>
              <sld:ColorMapEntry quantity="63.241920928955082" label="63.2419" color="#fcbba1"/>
              <sld:ColorMapEntry quantity="69.679169387817382" label="69.6792" color="#fc9272"/>
              <sld:ColorMapEntry quantity="76.116417846679695" label="76.1164" color="#fb6a4a"/>
              <sld:ColorMapEntry quantity="82.553666305541995" label="82.5537" color="#ef3b2c"/>
              <sld:ColorMapEntry quantity="88.990914764404295" label="88.9909" color="#cb181d"/>
              <sld:ColorMapEntry quantity="94.932990264892581" label="94.9330" color="#a50f15"/>
              <sld:ColorMapEntry quantity="99.884719848632813" label="99.8847" color="#67000d"/>
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>
