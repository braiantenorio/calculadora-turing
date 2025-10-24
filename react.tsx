import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, SkipForward, Settings } from 'lucide-react';

const TuringMachineVisualizer = () => {
  const [tape, setTape] = useState(['1', '1', '1', ' ']);
  const [head, setHead] = useState(0);
  const [state, setState] = useState('s0');
  const [isRunning, setIsRunning] = useState(false);
  const [speed, setSpeed] = useState(500);
  const [showSettings, setShowSettings] = useState(false);
  const [history, setHistory] = useState([]);
  const [stepCount, setStepCount] = useState(0);
  
  const finalState = 's2';
  
  const transitions = {
    's0-0': { newState: 's0', write: 'n', move: 'R' },
    's0-1': { newState: 's0', write: 'n', move: 'R' },
    's0- ': { newState: 's1', write: 'n', move: 'L' },
    's1-0': { newState: 's2', write: '1', move: 'N' },
    's1-1': { newState: 's3', write: '0', move: 'L' },
    's3-0': { newState: 's1', write: 'n', move: 'N' },
    's3-1': { newState: 's1', write: 'n', move: 'N' },
    's3- ': { newState: 's2', write: '1', move: 'L' },
  };

  const executeStep = () => {
    if (state === finalState) {
      setIsRunning(false);
      return false;
    }

    const symbol = tape[head];
    const key = `${state}-${symbol}`;
    const transition = transitions[key];

    if (!transition) {
      setIsRunning(false);
      return false;
    }

    const newTape = [...tape];
    if (transition.write !== 'n') {
      newTape[head] = transition.write;
    }

    let newHead = head;
    if (transition.move === 'R') {
      newHead = head + 1;
      if (newHead >= newTape.length) {
        newTape.push(' ');
      }
    } else if (transition.move === 'L') {
      newHead = head - 1;
      if (newHead < 0) {
        newTape.unshift(' ');
        newHead = 0;
      }
    }

    setHistory(prev => [...prev, { tape: [...tape], head, state }]);
    setTape(newTape);
    setHead(newHead);
    setState(transition.newState);
    setStepCount(prev => prev + 1);
    
    return true;
  };

  useEffect(() => {
    if (isRunning && state !== finalState) {
      const timer = setTimeout(() => {
        if (!executeStep()) {
          setIsRunning(false);
        }
      }, speed);
      return () => clearTimeout(timer);
    }
  }, [isRunning, state, tape, head, speed]);

  const reset = () => {
    setTape(['1', '1', '1', ' ']);
    setHead(0);
    setState('s0');
    setIsRunning(false);
    setHistory([]);
    setStepCount(0);
  };

  const handleInputChange = (value) => {
    const cleanValue = value.replace(/[^01]/g, '');
    setTape([...cleanValue.split(''), ' ']);
    setHead(0);
    setState('s0');
    setHistory([]);
    setStepCount(0);
  };

  const tapeDisplay = tape.map((symbol, index) => {
    const isHead = index === head;
    return (
      <div
        key={index}
        className={`
          w-14 h-14 border-2 flex items-center justify-center font-mono text-xl
          transition-all duration-300
          ${isHead 
            ? 'border-blue-500 bg-blue-100 scale-110 shadow-lg' 
            : 'border-gray-300 bg-white'
          }
        `}
      >
        {symbol === ' ' ? '□' : symbol}
      </div>
    );
  });

  const stateColor = state === finalState ? 'bg-green-500' : 'bg-blue-500';

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Máquina de Turing - Incrementador
          </h1>
          <p className="text-gray-600 mb-8">Incrementa números binarios en 1</p>

          {/* Estado actual */}
          <div className="mb-8 flex items-center gap-4">
            <div className="flex items-center gap-3">
              <span className="text-gray-700 font-semibold">Estado:</span>
              <span className={`${stateColor} text-white px-4 py-2 rounded-lg font-mono text-lg`}>
                {state}
              </span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-700 font-semibold">Pasos:</span>
              <span className="bg-gray-200 px-4 py-2 rounded-lg font-mono text-lg">
                {stepCount}
              </span>
            </div>
            {state === finalState && (
              <span className="ml-auto bg-green-100 text-green-700 px-4 py-2 rounded-lg font-semibold">
                ✓ Finalizado
              </span>
            )}
          </div>

          {/* Cinta */}
          <div className="mb-8 overflow-x-auto">
            <div className="flex gap-1 justify-center min-w-max py-4">
              {tapeDisplay}
            </div>
          </div>

          {/* Controles */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div>
              <label className="block text-gray-700 font-semibold mb-2">
                Número binario inicial:
              </label>
              <input
                type="text"
                placeholder="Ej: 1011"
                className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 font-mono text-lg focus:outline-none focus:border-blue-500"
                onChange={(e) => handleInputChange(e.target.value)}
                disabled={isRunning}
              />
            </div>

            <div className="flex items-end gap-2">
              <button
                onClick={() => setIsRunning(!isRunning)}
                disabled={state === finalState}
                className={`
                  flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-lg
                  font-semibold text-white transition-all
                  ${state === finalState 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : isRunning 
                      ? 'bg-orange-500 hover:bg-orange-600' 
                      : 'bg-green-500 hover:bg-green-600'
                  }
                `}
              >
                {isRunning ? <Pause size={20} /> : <Play size={20} />}
                {isRunning ? 'Pausar' : 'Ejecutar'}
              </button>

              <button
                onClick={() => executeStep()}
                disabled={isRunning || state === finalState}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all"
              >
                <SkipForward size={20} />
                Paso
              </button>

              <button
                onClick={reset}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition-all"
              >
                <RotateCcw size={20} />
                Reset
              </button>

              <button
                onClick={() => setShowSettings(!showSettings)}
                className="flex items-center justify-center px-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all"
              >
                <Settings size={20} />
              </button>
            </div>
          </div>

          {/* Configuración de velocidad */}
          {showSettings && (
            <div className="bg-gray-50 rounded-lg p-6 mb-8">
              <label className="block text-gray-700 font-semibold mb-3">
                Velocidad de ejecución: {speed}ms
              </label>
              <input
                type="range"
                min="100"
                max="2000"
                step="100"
                value={speed}
                onChange={(e) => setSpeed(Number(e.target.value))}
                className="w-full"
              />
              <div className="flex justify-between text-sm text-gray-600 mt-2">
                <span>Rápido</span>
                <span>Lento</span>
              </div>
            </div>
          )}

          {/* Tabla de transiciones */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Tabla de Transiciones</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b-2 border-gray-300">
                    <th className="text-left py-2 px-4 font-semibold">Estado</th>
                    <th className="text-left py-2 px-4 font-semibold">Símbolo</th>
                    <th className="text-left py-2 px-4 font-semibold">→ Nuevo Estado</th>
                    <th className="text-left py-2 px-4 font-semibold">Escribir</th>
                    <th className="text-left py-2 px-4 font-semibold">Mover</th>
                  </tr>
                </thead>
                <tbody className="font-mono">
                  {Object.entries(transitions).map(([key, value]) => {
                    const [s, symbol] = key.split('-');
                    return (
                      <tr key={key} className="border-b border-gray-200 hover:bg-gray-100">
                        <td className="py-2 px-4">{s}</td>
                        <td className="py-2 px-4">{symbol === ' ' ? '□' : symbol}</td>
                        <td className="py-2 px-4">{value.newState}</td>
                        <td className="py-2 px-4">{value.write === 'n' ? '-' : value.write}</td>
                        <td className="py-2 px-4">{value.move}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TuringMachineVisualizer;
