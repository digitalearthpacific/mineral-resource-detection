<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0" xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint/>
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>lulc_2023</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="values">
              <sld:ColorMapEntry quantity="1" opacity="0.596078" label="1" color="#d58357"/>
              <sld:ColorMapEntry quantity="2" opacity="0" label="2" color="#3a7c58"/>
              <sld:ColorMapEntry quantity="3" opacity="0" label="3" color="#ffd901"/>
              <sld:ColorMapEntry quantity="4" opacity="0" label="4" color="#b0fb47"/>
              <sld:ColorMapEntry quantity="5" opacity="0" label="5" color="#cdcdcd"/>
              <sld:ColorMapEntry quantity="6" opacity="0" label="6" color="#4cbca0"/>
              <sld:ColorMapEntry quantity="7" opacity="0.498039" label="7" color="#4197ed"/>
              <sld:ColorMapEntry quantity="8" label="8" color="#f71509"/>
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>
