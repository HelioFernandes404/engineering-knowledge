package org.helio.cartorioapi.controllers;

import org.helio.cartorioapi.dto.AtribuicaosDTO;
import org.helio.cartorioapi.dto.AtribuicaosMinDTO;
import org.helio.cartorioapi.services.AtribuicaosServices;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import javax.validation.Valid;
import java.net.URI;

@RestController
@RequestMapping("/atribuicoes")
public class AtribuicaosController {

    @Autowired
    private AtribuicaosServices service;

    @GetMapping
    public ResponseEntity<Page<AtribuicaosMinDTO>> findAll(@RequestParam(defaultValue = "0") int page) {
        Pageable pageable = PageRequest.of(page, 10, Sort.by("id").ascending());
        Page<AtribuicaosMinDTO> dto = service.findAll(pageable);
        return ResponseEntity.ok(dto);
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<AtribuicaosDTO> findById(@PathVariable String id) {
        AtribuicaosDTO dto = service.findById(id);
        return ResponseEntity.ok(dto);
    }

    @PostMapping
    public ResponseEntity<AtribuicaosDTO> insert(@Valid @RequestBody AtribuicaosDTO dto) {
        dto = service.insert(dto);
        URI uri = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}")
                .buildAndExpand(dto.getId()).toUri();
        return ResponseEntity.created(uri).body(dto);
    }

    @PutMapping(value = "/{id}")
    public ResponseEntity<AtribuicaosDTO> update(@PathVariable String id, @Valid @RequestBody AtribuicaosDTO dto) {
        dto = service.update(id, dto);
        return ResponseEntity.ok(dto);
    }

    @DeleteMapping(value = "/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
