local glyph = node.id('glyph')
local hlist = node.id('hlist')
local vlist = node.id('vlist')
local glue = node.id('glue')
local kern = node.id('kern')
local penalty = node.id('penalty')
local disc = node.id('disc')
local rule = node.id('rule')

local debug = true
local unicode = true

local charmap = {}
charmap[0x0B] = "ff"
charmap[0x0C] = "fi"
charmap[0x0D] = "fl"
charmap[0x0E] = "ffi"
charmap[0x0F] = "ffl"
charmap[0x10] = "i"
charmap[0x11] = "j"
if unicode then
  charmap[0x1A] = "æ"
  charmap[0x22] = "”"
  charmap[0x27] = "’"
  charmap[0x5C] = "“"
  charmap[0x7B] = "–"
  charmap[0x7C] = "—"
else
  charmap[0x1A] = "ae"
  charmap[0x22] = '"'
  charmap[0x27] = "'"
  charmap[0x5C] = '"'
  charmap[0x7B] = "-"
  charmap[0x7C] = "--"
end

-- https://github.com/Stepets/utf8.lua/blob/master/utf8.lua
local function utf8char(unicode)
  if unicode <= 0x7F then return string.char(unicode) end

  if (unicode <= 0x7FF) then
    local Byte0 = 0xC0 + math.floor(unicode / 0x40);
    local Byte1 = 0x80 + (unicode % 0x40);
    return string.char(Byte0, Byte1);
  end;

  if (unicode <= 0xFFFF) then
    local Byte0 = 0xE0 +  math.floor(unicode / 0x1000);
    local Byte1 = 0x80 + (math.floor(unicode / 0x40) % 0x40);
    local Byte2 = 0x80 + (unicode % 0x40);
    return string.char(Byte0, Byte1, Byte2);
  end;

  if (unicode <= 0x10FFFF) then
    local code = unicode
    local Byte3= 0x80 + (code % 0x40);
    code       = math.floor(code / 0x40)
    local Byte2= 0x80 + (code % 0x40);
    code       = math.floor(code / 0x40)
    local Byte1= 0x80 + (code % 0x40);
    code       = math.floor(code / 0x40)
    local Byte0= 0xF0 + code;

    return string.char(Byte0, Byte1, Byte2, Byte3);
  end;

  error 'Unicode cannot be greater than U+10FFFF!'
end

local accents = require(gamekilib .. "/accents")

local spaces_pending = 0
local eat_spaces = false
local accent_mode = false
local accent

function gothru(h,prof)
  for t in node.traverse(h) do
    if debug then texio.write_nl(string.rep("...",prof) .. 'NODE type=' ..  node.type(t.id) .. ' subtype=' .. t.subtype ) end
    if t.id == hlist or t.id == vlist then
      --texio.write(' w=' .. t.width .. ' h=' .. t.height .. ' d=' .. t.depth .. ' s=' .. t.shift )
      gothru(t.list,prof+1)
    end
    if t.id == disc then
      if t.replace then
        if debug then texio.write(' => ' .. node.type(t.replace.id)) end
        t = t.replace
      end
      eat_spaces = false
    end
    if t.id == glyph then
      if debug then texio.write(' font=' .. t.font .. ' char=' .. utf8char(t.char) .. ' (' .. string.format('0x%X', t.char) .. ')') end
      if spaces_pending > 0 then
        for i=1,spaces_pending do
          io.write(" ")
        end
	spaces_pending = 0
      end
      eat_spaces = false

      if accent_mode then
        if unicode and accents[t.char] then
	  accent = accents[t.char]
	end
      else
        local char
	if t.subtype == 256 then
	  char = utf8char(t.char)
        elseif charmap[t.char] then
          char = charmap[t.char]
        else
          char = string.char(t.char)
        end
        if accent then
          io.write(accent[char])
          accent = null
        else
          io.write(char)
        end
      end
    end
    if t.id == kern then
      if t.subtype == 2 then
        -- Accent kerning
        accent_mode = not accent_mode
      end
    end
    if t.id == glue then
      if debug then
        texio.write(' w=' .. t.spec.width .. ' stretch=' .. t.spec.stretch)
	if eat_spaces then texio.write(' eat_spaces') end
      end
      if (t.subtype == 0 and (t.spec.width > 0 or t.spec.stretch > 0)
          and not eat_spaces) then
        spaces_pending = spaces_pending + 1
      end
    end
    if t.id == penalty then
      if debug then texio.write(' penalty=' .. t.penalty) end
      if t.penalty == -10000 then
        io.write("\n")
	spaces_pending = 0
	eat_spaces = true
      end
    end
    if t.id == rule then
      if spaces_pending > 0 then
        for i=1,spaces_pending do
          io.write(" ")
        end
	spaces_pending = 0
      end
      io.write("_")
    end
  end
end

local first = true

process = function (head, groupcode)
  if debug then texio.write_nl('Process: ' .. groupcode) end
  if first then
    first = false
  else
    io.write("\n")
  end
  gothru(head, 0)
  io.write("\n")
  return true
end

openout = function (filename)
  local outputdir
  for k,v in pairs(arg) do
    if v:find('%-output%-directory') then
      if v:find('%-output%-directory=') then
        outputdir=string.explode(v, '=')[2]
      else
        outputdir=arg[tonumber(k)+1]
      end
    end
  end
  if outputdir then
    io.output(outputdir .. "/" .. filename)
  else
    io.output(filename)
  end
end

luatexbase.add_to_callback("pre_linebreak_filter", process, "process")
