import { describe, it, expect } from "vitest";
import { inspectNavigation, inspectSegment, type NavigationGrid } from "../src/lib/mapNavigation";

function fixture(): NavigationGrid {
  return { width:16,height:16,cell_game_units:32,bits:["walk","blocked","trees","cliffs","ramps","uncertain"],cells:new Uint8Array(256).fill(1),heights:new Uint8Array(256).fill(10) };
}
describe("map navigation conservative route checks",()=>{
  it("uses north-up world cell centres and preserves simultaneous evidence",()=>{
    const grid=fixture(); grid.cells[0]=2|8; grid.heights[0]=11;
    expect(inspectNavigation(grid,{x:0,y:0})).toEqual({flags:["blocked","cliffs"],layer:11,world:[-8176,8176]});
    expect(inspectNavigation(grid,{x:-.1,y:0})).toBeNull();
    expect(inspectNavigation(grid,{x:16,y:0})).toBeNull();
  });
  it("detects thin barriers between endpoints, trees and unknown unit occupancy",()=>{
    const grid=fixture(); grid.cells[8*16+8]=2; grid.cells[8*16+10]=4; grid.cells[8*16+12]=32;
    expect(inspectSegment(grid,{x:3,y:8},{x:13,y:8})).toEqual(expect.arrayContaining(["blocked","trees","uncertain"]));
  });
  it("checks clearance beside the centre line and both endpoint margins",()=>{
    const grid=fixture(); grid.cells[9*16+8]=4;
    expect(inspectSegment(grid,{x:3,y:8},{x:12,y:8})).toContain("trees");
    expect(inspectSegment(grid,{x:0,y:0},{x:0,y:0})).toContain("outside");
  });
  it("does not reject an open ramp or invent route clearance from a different location",()=>{
    const grid=fixture();grid.cells[8*16+8]=1|16; grid.cells[2*16+8]=2;
    expect(inspectSegment(grid,{x:3,y:8},{x:12,y:8})).toEqual([]);
    expect(inspectSegment(grid,{x:3,y:2},{x:12,y:2})).toContain("blocked");
  });
});
