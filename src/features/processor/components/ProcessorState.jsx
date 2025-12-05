import { useState, useEffect, useCallback, memo } from 'react';
import { Cpu, Database, Flag } from 'lucide-react';
import { useProcessorRegisters, useProcessorFlags, useProcessorMemory } from '../stores/processorStore';
import './ProcessorState.css';

const HIGHLIGHT_DURATION = 600;

function ProcessorState() {
  const registers = useProcessorRegisters();
  const flags = useProcessorFlags();
  const memory = useProcessorMemory();
  const [changedRegisters, setChangedRegisters] = useState(new Set());
  const [changedFlags, setChangedFlags] = useState(new Set());
  const [prevState, setPrevState] = useState({ registers: {}, flags: {} });

  useEffect(() => {
    const regChanges = new Set();
    const flagChanges = new Set();

    Object.keys(registers).forEach(reg => {
      if (prevState.registers[reg] !== registers[reg]) {
        regChanges.add(reg);
      }
    });

    Object.keys(flags).forEach(flag => {
      if (prevState.flags[flag] !== flags[flag]) {
        flagChanges.add(flag);
      }
    });

    if (regChanges.size > 0 || flagChanges.size > 0) {
      setChangedRegisters(regChanges);
      setChangedFlags(flagChanges);

      setTimeout(() => {
        setChangedRegisters(new Set());
        setChangedFlags(new Set());
      }, HIGHLIGHT_DURATION);
    }

    setPrevState({ registers, flags });
  }, [registers, flags]);

  const hexToDec = useCallback((hex) => {
    if (!hex || typeof hex !== 'string') return 0;
    try {
      const cleanHex = hex.replace(/[Hh]$/, '').replace(/^0x/i, '');
      const result = parseInt(cleanHex, 16);
      return isNaN(result) ? 0 : result;
    } catch (error) {
      return 0;
    }
  }, []);

  const hexToBin = useCallback((hex) => {
    if (!hex || typeof hex !== 'string') return '00000000';
    try {
      const cleanHex = hex.replace(/[Hh]$/, '').replace(/^0x/i, '');
      const result = parseInt(cleanHex, 16);
      return isNaN(result) ? '00000000' : result.toString(2).padStart(8, '0');
    } catch (error) {
      return '00000000';
    }
  }, []);

  const renderRegisterRow = useCallback((name, value) => {
    const isChanged = changedRegisters.has(name);
    return (
      <tr key={name} className={isChanged ? 'changed' : ''}>
        <td className="register-name">{name}</td>
        <td className="register-value">{value}</td>
        <td className="register-decimal">{hexToDec(value)}</td>
      </tr>
    );
  }, [changedRegisters, hexToDec]);

  const renderMemoryView = useCallback(() => {
    if (!memory || typeof memory !== 'object') {
      return (
        <tr>
          <td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-tertiary)' }}>
            No memory data available yet. Run some code to populate memory.
          </td>
        </tr>
      );
    }
    
    const memoryEntries = Object.entries(memory);
    
    if (memoryEntries.length === 0) {
      return (
        <tr>
          <td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-tertiary)' }}>
            No memory data available yet. Run some code to populate memory.
          </td>
        </tr>
      );
    }

    return memoryEntries
      .sort(([a], [b]) => {
        try {
          const cleanA = String(a).replace(/[Hh]$/, '').replace(/^0x/i, '');
          const cleanB = String(b).replace(/[Hh]$/, '').replace(/^0x/i, '');
          const numA = parseInt(cleanA, 16);
          const numB = parseInt(cleanB, 16);
          
          if (isNaN(numA) || isNaN(numB)) {
            // Fallback to string comparison if not valid hex
            return String(a).localeCompare(String(b));
          }
          
          return numA - numB;
        } catch (error) {
          return 0;
        }
      })
      .map(([address, value]) => {
        try {
          const decimalValue = hexToDec(value);
          
          return (
            <tr key={address}>
              <td className="memory-addr">{address}</td>
              <td className="memory-cell">{value}</td>
              <td className="memory-decimal">{decimalValue}</td>
              <td className="memory-binary">{hexToBin(value)}</td>
            </tr>
          );
        } catch (error) {
          return (
            <tr key={address}>
              <td className="memory-addr">{address}</td>
              <td className="memory-cell">{value}</td>
              <td className="memory-decimal">Error</td>
              <td className="memory-binary">Error</td>
            </tr>
          );
        }
      });
  }, [memory, hexToDec, hexToBin]);

  return (
    <div className="processor-state">
      <div className="processor-state-header">
        <Cpu size={20} />
        <h2>Processor State</h2>
      </div>

      <div className="processor-state-content">
        {/* Registers Section */}
        <div className="state-section">
          <div className="section-header">
            <Database size={18} />
            <h3>Registers</h3>
          </div>
          <div className="registers-grid">
            <div className="register-group">
              <h4>8-bit Registers</h4>
              <table className="registers-table">
                <thead>
                  <tr>
                    <th>Reg</th>
                    <th>Hex</th>
                    <th>Dec</th>
                  </tr>
                </thead>
                <tbody>
                  {renderRegisterRow('A', registers.A)}
                  {renderRegisterRow('B', registers.B)}
                  {renderRegisterRow('C', registers.C)}
                  {renderRegisterRow('D', registers.D)}
                  {renderRegisterRow('E', registers.E)}
                  {renderRegisterRow('H', registers.H)}
                  {renderRegisterRow('L', registers.L)}
                </tbody>
              </table>
            </div>
            
            <div className="register-group">
              <h4>16-bit Registers</h4>
              <table className="registers-table">
                <thead>
                  <tr>
                    <th>Reg</th>
                    <th>Hex</th>
                    <th>Dec</th>
                  </tr>
                </thead>
                <tbody>
                  {renderRegisterRow('PC', registers.PC)}
                  {renderRegisterRow('SP', registers.SP)}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Flags Section */}
        <div className="state-section">
          <div className="section-header">
            <Flag size={18} />
            <h3>Flags</h3>
          </div>
          <table className="flags-table-horizontal">
            <thead>
              <tr>
                {Object.keys(flags).map(flag => (
                  <th key={flag}>{flag}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {Object.entries(flags).map(([flag, value]) => (
                  <td key={flag} className={value ? 'flag-set' : 'flag-clear'}>
                    {value ? '1' : '0'}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>

        {/* Memory Section */}
        <div className="state-section">
          <div className="section-header">
            <Database size={18} />
            <h3>Memory</h3>
          </div>
          <div className="memory-table-container">
            <table className="memory-table">
              <thead>
                <tr>
                  <th>Address</th>
                  <th>Hex</th>
                  <th>Decimal</th>
                  <th>Binary</th>
                </tr>
              </thead>
              <tbody>
                {renderMemoryView()}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProcessorState;
