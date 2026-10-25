import React from 'react';
import {Composition} from 'remotion';
import {JerpFilm} from './JerpFilm';
export const RemotionRoot:React.FC=()=> <Composition id='JerpFilm' component={JerpFilm} durationInFrames={1470} fps={30} width={1920} height={1080}/>;
