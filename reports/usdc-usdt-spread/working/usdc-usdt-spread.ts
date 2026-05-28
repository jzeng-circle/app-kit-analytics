import 'dotenv/config'
import { inspect } from 'util'
import { AppKit } from '@circle-fin/app-kit'
import { createViemAdapterFromPrivateKey } from '@circle-fin/adapter-viem-v2'
import { createSolanaAdapterFromPrivateKey } from '@circle-fin/adapter-solana'

const evmPrivateKey = process.env['PRIVATE_KEY'] as `0x${string}`
const solanaPrivateKey = process.env['SOLANA_PRIVATE_KEY'] as string
const kitKey = process.env['KIT_KEY'] as string

const TOKEN_IN = 'USDC' as const
const TOKEN_OUT = 'USDT' as const

const TEST_AMOUNTS = [
  '100',
  '10000',
  '50000',
  '100000',
  '200000',
  '300000',
  '400000',
  '500000',
  '1000000',
] as const

const BENCHMARK_AMOUNT = '100'

// Sweep all amounts once per pass; do SWEEPS passes total. Interleaving ensures
// every amount within a sweep is sampled in the same ~tens-of-seconds window.
// IMPORTANT: spread bips are computed PER SWEEP (using that sweep's $1 quote
// as the benchmark for all other amounts in that sweep), then averaged across
// sweeps. This is robust against intra-test market drift — each sweep's
// benchmark uses the same market snapshot as its other samples.
const SWEEPS = 3

const buildAdapter = (chain: string) => {
  if (chain === 'Solana') {
    return createSolanaAdapterFromPrivateKey({ privateKey: solanaPrivateKey })
  }
  return createViemAdapterFromPrivateKey({ privateKey: evmPrivateKey })
}

const main = async (): Promise<void> => {
  const chain = process.argv[2]
  if (!chain) {
    console.error('Usage: tsx swap/usdc-usdt-spread.ts <Chain>   e.g. Ethereum | Solana | Avalanche')
    process.exit(1)
  }

  const kit = new AppKit()
  const adapter = buildAdapter(chain)

  // sweeps[i] is a map from amountIn -> amountOut number for sweep i+1.
  const sweeps: Array<Map<string, number>> = []

  for (let sweep = 1; sweep <= SWEEPS; sweep++) {
    const sweepResults = new Map<string, number>()
    console.log(`\n##################### SWEEP ${sweep}/${SWEEPS} on ${chain} #####################`)
    for (const amountIn of TEST_AMOUNTS) {
      console.log(`\n--- estimateSwap ${amountIn} ${TOKEN_IN} -> ${TOKEN_OUT} (sweep ${sweep}) ---`)
      try {
        const estimate = await kit.estimateSwap({
          from: { adapter: adapter as any, chain: chain as any },
          tokenIn: TOKEN_IN,
          tokenOut: TOKEN_OUT,
          amountIn,
          config: { kitKey, slippageBps: 0 },
        })
        console.log(inspect(estimate, false, null, true))
        sweepResults.set(amountIn, Number(estimate.estimatedOutput.amount))
      } catch (err) {
        console.log('ERROR', amountIn, 'sweep', sweep, inspect(err, false, null, true))
      }
      await new Promise((r) => setTimeout(r, 2_000))
    }
    sweeps.push(sweepResults)
  }

  // Per-sweep bips: each sweep computes its own internal spread vs its own $1
  // quote. Then we average bips across sweeps per amount.
  const perSweepBips: Map<string, number[]> = new Map()
  for (const a of TEST_AMOUNTS) perSweepBips.set(a, [])

  for (let s = 0; s < sweeps.length; s++) {
    const sweep = sweeps[s]
    const benchOut = sweep.get(BENCHMARK_AMOUNT)
    if (benchOut === undefined) {
      console.log(`Sweep ${s + 1} missing $${BENCHMARK_AMOUNT} benchmark — skipping its bips contribution`)
      continue
    }
    const benchRate = benchOut / Number(BENCHMARK_AMOUNT)
    for (const amountIn of TEST_AMOUNTS) {
      const out = sweep.get(amountIn)
      if (out === undefined) continue
      const rate = out / Number(amountIn)
      const bips = ((benchRate - rate) / benchRate) * 10_000
      perSweepBips.get(amountIn)!.push(bips)
    }
  }

  console.log('\n========================= SPREAD ANALYSIS (per-sweep bips, averaged) =========================')
  console.log(`Pair: ${TOKEN_IN} -> ${TOKEN_OUT} on ${chain}`)
  console.log(`Sweeps: ${SWEEPS}`)
  console.log(`Method: bips = ((sweep_$${BENCHMARK_AMOUNT}_rate - sweep_N_rate) / sweep_$${BENCHMARK_AMOUNT}_rate) * 10_000, computed per sweep using that sweep's own $${BENCHMARK_AMOUNT} quote as benchmark. Then averaged across sweeps.`)
  console.log('')
  console.log(
    'amountIn'.padStart(10) + ' | ' +
    'sweep 1 amountOut'.padStart(20) + ' | ' +
    'sweep 2 amountOut'.padStart(20) + ' | ' +
    'sweep 3 amountOut'.padStart(20) + ' | ' +
    'sweep 1 bips'.padStart(14) + ' | ' +
    'sweep 2 bips'.padStart(14) + ' | ' +
    'sweep 3 bips'.padStart(14) + ' | ' +
    'avg bips'.padStart(10)
  )
  console.log('-'.repeat(160))
  for (const amountIn of TEST_AMOUNTS) {
    const out1 = sweeps[0]?.get(amountIn)
    const out2 = sweeps[1]?.get(amountIn)
    const out3 = sweeps[2]?.get(amountIn)
    const bipsArr = perSweepBips.get(amountIn)!
    const avgBips = bipsArr.length === 0 ? NaN : bipsArr.reduce((s, n) => s + n, 0) / bipsArr.length
    const fmtOut = (n: number | undefined) => (n === undefined ? 'n/a' : n.toFixed(6))
    const fmtBips = (n: number | undefined) => (n === undefined || Number.isNaN(n) ? 'n/a' : n.toFixed(2))
    console.log(
      amountIn.padStart(10) +
      ' | ' + fmtOut(out1).padStart(20) +
      ' | ' + fmtOut(out2).padStart(20) +
      ' | ' + fmtOut(out3).padStart(20) +
      ' | ' + fmtBips(bipsArr[0]).padStart(14) +
      ' | ' + fmtBips(bipsArr[1]).padStart(14) +
      ' | ' + fmtBips(bipsArr[2]).padStart(14) +
      ' | ' + fmtBips(avgBips).padStart(10)
    )
  }
  console.log('==================================================================================================')
}

main().catch((err) => {
  console.log('FATAL', inspect(err, false, null, true))
  process.exit(1)
})
